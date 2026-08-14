# horizontal_state.py | Time-stamp: 26-0812-1939
"""State transition controller for the horizontal (time) axis."""

from dataclasses import dataclass

import torch
from torch import Tensor, nn


@dataclass(frozen=True, slots=True)
class TransitionResult:
    """Observable outputs of one horizontal-state transition."""

    state: Tensor
    update_gate: Tensor
    retention_gate: Tensor


class HorizontalStateController(nn.Module):
    """Combine a vertical inference vector with the preceding temporal state.

    The sigmoid update gate selects, element by element, how much of the new
    candidate enters the state. Its complement is the retention rate.
    """

    def __init__(self, hidden_dim: int, decay_threshold: float = 1.0e-6) -> None:
        super().__init__()
        if hidden_dim <= 0:
            raise ValueError("hidden_dim must be greater than zero")
        if not 0.0 <= decay_threshold < 1.0:
            raise ValueError("decay_threshold must be in [0, 1)")

        self.hidden_dim = hidden_dim
        self.decay_threshold = decay_threshold
        joined_dim = hidden_dim * 2
        self.gate_layer = nn.Linear(joined_dim, hidden_dim)
        self.candidate_layer = nn.Linear(joined_dim, hidden_dim)

    def forward(self, vertical_output: Tensor, previous_state: Tensor) -> TransitionResult:
        """Advance the horizontal state by exactly one discrete time step."""
        self._validate_input("vertical_output", vertical_output)
        self._validate_input("previous_state", previous_state)
        if vertical_output.shape != previous_state.shape:
            raise ValueError("vertical_output and previous_state must have equal shapes")
        if vertical_output.device != previous_state.device:
            raise ValueError("vertical_output and previous_state must share a device")
        if vertical_output.dtype != previous_state.dtype:
            raise ValueError("vertical_output and previous_state must share a dtype")

        combined = torch.cat((vertical_output, previous_state), dim=-1)
        update_gate = torch.sigmoid(self.gate_layer(combined))
        retention_gate = 1.0 - update_gate

        # Explicitly prune only numerically negligible retention. The default
        # threshold is deliberately small so this PoC does not erase history.
        effective_retention = torch.where(
            retention_gate < self.decay_threshold,
            torch.zeros_like(retention_gate),
            retention_gate,
        )
        candidate = torch.tanh(self.candidate_layer(combined))
        new_state = effective_retention * previous_state + update_gate * candidate

        if not torch.isfinite(new_state).all():
            raise FloatingPointError("state transition produced a non-finite value")

        return TransitionResult(
            state=new_state,
            update_gate=update_gate,
            retention_gate=effective_retention,
        )

    def _validate_input(self, name: str, value: Tensor) -> None:
        if value.ndim != 2:
            raise ValueError(f"{name} must have shape [batch, hidden_dim]")
        if value.shape[-1] != self.hidden_dim:
            raise ValueError(
                f"{name} last dimension must be {self.hidden_dim}, got {value.shape[-1]}"
            )
        if not value.is_floating_point():
            raise TypeError(f"{name} must be a floating-point tensor")
        if not torch.isfinite(value).all():
            raise ValueError(f"{name} contains a non-finite value")

