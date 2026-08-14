# config.py | Time-stamp: 26-0812-1939
"""Configuration values for the horizontal-state proof of concept."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PoCConfig:
    """Immutable runtime configuration for a single PoC execution."""

    hidden_dim: int = 768
    decay_threshold: float = 1.0e-6
    db_path: Path = Path(__file__).resolve().parent / "horizontal_state.db"
    sequence_start: int = 0
    sequence_end: int = 10
    random_seed: int = 42

    def validate(self) -> None:
        """Fail early when a configuration cannot produce a valid run."""
        if self.hidden_dim <= 0:
            raise ValueError("hidden_dim must be greater than zero")
        if not 0.0 <= self.decay_threshold < 1.0:
            raise ValueError("decay_threshold must be in [0, 1)")
        if self.sequence_start > self.sequence_end:
            raise ValueError("sequence_start must not exceed sequence_end")

