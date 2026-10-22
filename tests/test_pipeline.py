"""Check data contracts, reproducibility, and end-to-end artifact generation."""

import numpy as np
import pandas as pd
import pytest

from src.analysis import FEATURES, fit_clusters, run_pipeline
from src.generate_data import generate_sessions


def test_synthetic_data_contract():
    frame = generate_sessions()
    assert len(frame) == 120
    assert frame.session_id.is_unique
    assert not frame.isna().any().any()
    assert (frame.task_time_seconds > 0).all()
    for column in ["error_count", "hesitation_count"]:
        assert (frame[column] >= 0).all()
        assert (frame[column] % 1 == 0).all()
    for column in ["help_needed", "task_completed"]:
        assert set(frame[column]) == {0, 1}
    assert frame.perceived_ease.between(1, 7).all()
    pd.testing.assert_frame_equal(frame, generate_sessions())
    assert not frame.equals(generate_sessions(seed=43))
    with pytest.raises(ValueError):
        generate_sessions(0)


def test_cluster_selection_and_scaling():
    scaled, model, scores = fit_clusters(generate_sessions())
    assert scaled.shape == (120, len(FEATURES))
    np.testing.assert_allclose(scaled.mean(axis=0), 0, atol=1e-12)
    np.testing.assert_allclose(scaled.std(axis=0), 1)
    assert scores.k.tolist() == [2, 3, 4, 5, 6]
    assert scores.silhouette_score.between(-1, 1).all()
    assert model.n_clusters == scores.loc[scores.silhouette_score.idxmax(), "k"]
    np.testing.assert_array_equal(model.labels_, fit_clusters(generate_sessions())[1].labels_)


def test_end_to_end(tmp_path):
    frame, _ = run_pipeline(tmp_path)
    saved = pd.read_csv(tmp_path / "data/synthetic_pix_sessions.csv")
    assert len(saved) == 120
    summary = pd.read_csv(tmp_path / "outputs/cluster_indicators.csv")
    assert summary.session_count.sum() == 120
    assert frame.cluster.nunique() == len(summary)
    assert len(list((tmp_path / "outputs").glob("*.png"))) == 6
    assert "synthetic" in (tmp_path / "outputs/report.md").read_text().lower()
