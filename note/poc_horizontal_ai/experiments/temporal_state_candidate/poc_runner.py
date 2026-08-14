# poc_runner.py | Time-stamp: 26-0812-1939
"""Execute and verify the horizontal-state PoC for t=0 through t=10."""

from __future__ import annotations

import hashlib
import logging
from uuid import uuid4

import numpy as np
import torch

from config import PoCConfig
from horizontal_state import HorizontalStateController
from memory_store import HorizontalMemoryRepository


LOGGER = logging.getLogger("poc_horizontal_ai")


def state_hash(state: np.ndarray) -> str:
    """Create a stable chain identifier from a normalized float32 state."""
    normalized = np.ascontiguousarray(state, dtype=np.float32)
    return hashlib.sha256(normalized.tobytes(order="C")).hexdigest()


def make_vertical_sequence(config: PoCConfig) -> list[torch.Tensor]:
    """Build a deterministic, temporally varying pseudo-inference sequence."""
    generator = torch.Generator().manual_seed(config.random_seed)
    basis = torch.linspace(-1.0, 1.0, config.hidden_dim).unsqueeze(0)
    sequence: list[torch.Tensor] = []
    for step in range(config.sequence_start, config.sequence_end + 1):
        periodic = torch.sin(basis * (step + 1) * 0.35)
        noise = torch.randn((1, config.hidden_dim), generator=generator) * 0.02
        sequence.append(periodic + noise)
    return sequence


def execute_poc(config: PoCConfig) -> tuple[str, list[np.ndarray]]:
    config.validate()
    torch.manual_seed(config.random_seed)
    controller = HorizontalStateController(
        hidden_dim=config.hidden_dim,
        decay_threshold=config.decay_threshold,
    )
    controller.eval()

    run_id = uuid4().hex
    previous_state = torch.zeros((1, config.hidden_dim), dtype=torch.float32)
    expected_states: list[np.ndarray] = []

    with HorizontalMemoryRepository(config.db_path) as repository, torch.no_grad():
        for step, vertical_output in zip(
            range(config.sequence_start, config.sequence_end + 1),
            make_vertical_sequence(config),
            strict=True,
        ):
            previous_array = previous_state.squeeze(0).cpu().numpy().copy()
            transition = controller(vertical_output, previous_state)
            current_array = transition.state.squeeze(0).cpu().numpy().copy()
            gate_mean = float(transition.update_gate.mean().item())
            retention_mean = float(transition.retention_gate.mean().item())

            repository.append(
                run_id=run_id,
                step=step,
                state=current_array,
                gate_mean=gate_mean,
                retention_mean=retention_mean,
                metadata={
                    "previous_state_sha256": state_hash(previous_array),
                    "state_sha256": state_hash(current_array),
                    "vertical_norm": float(torch.linalg.vector_norm(vertical_output).item()),
                },
            )
            expected_states.append(current_array)
            previous_state = transition.state.detach()
            LOGGER.info(
                "t=%02d state_norm=%.6f update=%.6f retention=%.6f",
                step,
                float(torch.linalg.vector_norm(previous_state).item()),
                gate_mean,
                retention_mean,
            )

    return run_id, expected_states


def verify_persistence(config: PoCConfig, run_id: str, expected: list[np.ndarray]) -> None:
    """Re-open SQLite and verify persistence plus the complete state chain."""
    with HorizontalMemoryRepository(config.db_path) as repository:
        records = repository.get_run(run_id)
        latest = repository.get_latest(run_id)

    expected_count = config.sequence_end - config.sequence_start + 1
    assert len(records) == expected_count, "database record count mismatch"
    assert latest is not None and latest.step == config.sequence_end, "latest state mismatch"

    previous_hash = state_hash(np.zeros(config.hidden_dim, dtype=np.float32))
    for offset, record in enumerate(records):
        expected_step = config.sequence_start + offset
        assert record.step == expected_step, "state sequence contains a gap"
        assert record.state.shape == (config.hidden_dim,), "restored state shape mismatch"
        assert np.isfinite(record.state).all(), "restored state is non-finite"
        np.testing.assert_array_equal(record.state, expected[offset])
        assert record.metadata["previous_state_sha256"] == previous_hash, (
            "horizontal state chain is discontinuous"
        )
        current_hash = state_hash(record.state)
        assert record.metadata["state_sha256"] == current_hash, "state hash mismatch"
        assert 0.0 <= record.gate_mean <= 1.0, "update gate is outside [0, 1]"
        assert 0.0 <= record.retention_mean <= 1.0, "retention gate is outside [0, 1]"
        previous_hash = current_hash

    LOGGER.info("continuity verification: PASS (%d chained states)", len(records))
    LOGGER.info("persistence verification: PASS (%s)", config.db_path)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = PoCConfig()
    run_id, expected_states = execute_poc(config)
    verify_persistence(config, run_id, expected_states)
    LOGGER.info("PoC completed successfully: run_id=%s", run_id)


if __name__ == "__main__":
    main()

