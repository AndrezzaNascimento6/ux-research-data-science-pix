"""Generate synthetic sessions from continuous, overlapping behavioral variation."""

import numpy as np
import pandas as pd

SEED = 42


def generate_sessions(n_sessions=120, seed=SEED):
    """Return synthetic observations; no discrete user groups are sampled."""
    if n_sessions < 1:
        raise ValueError("n_sessions must be positive")
    rng = np.random.default_rng(seed)
    friction = rng.normal(0, 1, n_sessions)
    errors = rng.poisson(np.exp(0.1 + 0.35 * friction))
    hesitations = rng.poisson(np.exp(1.0 + 0.3 * friction))
    help_probability = 1 / (1 + np.exp(1.2 - 0.4 * friction - 0.15 * errors))
    help_needed = rng.binomial(1, help_probability)
    success_probability = 1 / (1 + np.exp(-2.4 + 0.4 * friction + 0.2 * errors))
    completed = rng.binomial(1, success_probability)
    elapsed = np.exp(4.5 + 0.2 * friction + rng.normal(0, 0.35, n_sessions))
    elapsed += 9 * errors + 5 * hesitations + 15 * help_needed
    ease = np.clip(np.rint(5.8 - 0.45 * friction - 0.3 * errors
                          - 0.4 * help_needed - 0.6 * (1 - completed)
                          + rng.normal(0, 1.0, n_sessions)), 1, 7).astype(int)
    return pd.DataFrame({
        "session_id": [f"S{i:03d}" for i in range(1, n_sessions + 1)],
        "task_time_seconds": elapsed.round(2),
        "error_count": errors,
        "hesitation_count": hesitations,
        "help_needed": help_needed,
        "task_completed": completed,
        "perceived_ease": ease,
    })
