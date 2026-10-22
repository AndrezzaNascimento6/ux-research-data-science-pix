"""Run reproducible exploratory analysis; clusters are descriptive partitions."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache" / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache"))
# Keep this small educational pipeline independent of host core discovery.
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler

from src.generate_data import SEED, generate_sessions

FEATURES = ["task_time_seconds", "error_count", "hesitation_count"]
METRICS = FEATURES + ["help_needed", "task_completed", "perceived_ease"]


def fit_clusters(frame):
    """Compare K=2..6 in standardized, log-transformed behavioral space."""
    transformed = np.log1p(frame[FEATURES])
    scaled = StandardScaler().fit_transform(transformed)
    models, rows = {}, []
    for k in range(2, 7):
        model = KMeans(n_clusters=k, random_state=SEED, n_init=30).fit(scaled)
        models[k] = model
        rows.append({"k": k, "silhouette_score": silhouette_score(scaled, model.labels_),
                     "inertia": model.inertia_})
    scores = pd.DataFrame(rows)
    best_k = int(scores.loc[scores.silhouette_score.idxmax(), "k"])
    return scaled, models[best_k], scores


def save_figure(figure, output, name):
    """Save a readable static artifact and release the figure."""
    figure.suptitle(figure._suptitle.get_text() + " | Synthetic data", fontsize=13)
    figure.tight_layout(rect=(0, 0, 1, 0.95))
    figure.savefig(output / name, dpi=160, bbox_inches="tight")
    plt.close(figure)


def run_pipeline(root=ROOT):
    """Regenerate data, tables, figures, and an English research report."""
    root = Path(root)
    data, output = root / "data", root / "outputs"
    data.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    frame = generate_sessions()
    frame.to_csv(data / "synthetic_pix_sessions.csv", index=False)
    frame[METRICS].describe().to_csv(output / "descriptive_statistics.csv")
    frame[METRICS].corr(method="spearman").to_csv(output / "spearman_correlations.csv")
    scaled, model, scores = fit_clusters(frame)
    scores.to_csv(output / "k_comparison.csv", index=False)
    frame["cluster"] = model.labels_
    frame["silhouette"] = silhouette_samples(scaled, model.labels_)
    frame.to_csv(output / "clustered_sessions.csv", index=False)
    summary = frame.groupby("cluster")[METRICS].mean()
    summary.insert(0, "session_count", frame.groupby("cluster").size())
    summary.to_csv(output / "cluster_indicators.csv")
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    for column, ax in zip(METRICS, axes.flat):
        sns.histplot(data=frame, x=column, discrete=column != FEATURES[0], ax=ax)
    fig.suptitle("Usability indicator distributions")
    save_figure(fig, output, "distributions.png")
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(frame[METRICS].corr(method="spearman"), annot=True, fmt=".2f",
                cmap="vlag", vmin=-1, vmax=1, ax=ax)
    fig.suptitle("Spearman correlations")
    save_figure(fig, output, "correlations.png")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(scores.k, scores.silhouette_score, marker="o")
    ax.set(xlabel="Number of clusters (K)", ylabel="Mean silhouette score", xticks=range(2, 7))
    fig.suptitle("K comparison in the full feature space")
    save_figure(fig, output, "k_comparison.png")
    pca = PCA(n_components=2).fit(scaled)
    coordinates = pca.transform(scaled)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.scatterplot(x=coordinates[:, 0], y=coordinates[:, 1], hue=frame.cluster.astype(str),
                    palette="colorblind", ax=axes[0])
    axes[0].set(xlabel=f"PC1 ({pca.explained_variance_ratio_[0]:.1%})",
                ylabel=f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    axes[0].legend(title="Cluster")
    sns.scatterplot(data=frame, x="task_time_seconds", y="hesitation_count",
                    hue=frame.cluster.astype(str), palette="colorblind", ax=axes[1])
    axes[1].legend(title="Cluster")
    fig.suptitle("Exploratory partitions (projection can hide overlap)")
    save_figure(fig, output, "clusters.png")
    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    for column, ax in zip(METRICS, axes.flat):
        if column in ["help_needed", "task_completed"]:
            ax.bar(summary.index.astype(str), summary[column], color="steelblue")
            ax.set(ylim=(0, 1), xlabel="Cluster", ylabel=f"{column} rate")
        else:
            sns.boxplot(data=frame, x="cluster", y=column, ax=ax, color="lightblue")
    fig.suptitle("Usability indicators by exploratory partition")
    save_figure(fig, output, "cluster_indicators.png")
    fig, ax = plt.subplots(figsize=(8, 5))
    offset = 0
    for cluster in sorted(frame.cluster.unique()):
        values = np.sort(frame.loc[frame.cluster == cluster, "silhouette"])
        ax.barh(np.arange(offset, offset + len(values)), values, height=1, label=str(cluster))
        offset += len(values) + 3
    ax.axvline(frame.silhouette.mean(), color="black", linestyle="--", label="Mean")
    ax.set(xlabel="Silhouette coefficient", ylabel="Sessions sorted within cluster", xlim=(-1, 1))
    ax.legend(title="Cluster")
    fig.suptitle("Individual silhouette diagnostics")
    save_figure(fig, output, "silhouette.png")
    best = scores.silhouette_score.max()
    runner_up = scores.silhouette_score.nlargest(2).iloc[1]
    report = f"""# Synthetic Pix usability: exploratory findings

All 120 sessions are synthetic. No actual participants or transfers were observed.

## Overall indicators

- Completion rate: {frame.task_completed.mean():.1%} (assistance allowed).
- Help-needed rate: {frame.help_needed.mean():.1%}.
- Median observed task time: {frame.task_time_seconds.median():.1f} seconds.
- Median completion time among completed sessions: {frame.loc[frame.task_completed == 1, 'task_time_seconds'].median():.1f} seconds.
- Mean perceived ease: {frame.perceived_ease.mean():.2f}/7.

## Clustering assessment

K={model.n_clusters} maximizes mean silhouette among K=2..6, with score {best:.3f}.
The improvement over the runner-up is only {best - runner_up:.3f}.
The selected K is {'at the edge of' if model.n_clusters in (2, 6) else 'inside'} the tested range;
it should not be treated as a globally optimal number of clusters.
Negative individual silhouettes: {(frame.silhouette < 0).mean():.1%}.
These diagnostics do not provide convincing evidence of distinct user profiles.
This numerical optimum is only a descriptive partition of a continuous synthetic
distribution. It does not establish distinct behavioral profiles or validated personas.
Inspect k_comparison.csv, silhouette.png and clusters.png together; a 2D projection
does not prove separation. No score threshold alone establishes real user segments.

Cluster means, sizes, completion/help rates and perceived ease are in
cluster_indicators.csv; distributions are shown in cluster_indicators.png.
Partition sizes range from {summary.session_count.min()} to {summary.session_count.max()} sessions.
Mean observed task times range from {summary.task_time_seconds.min():.1f} to
{summary.task_time_seconds.max():.1f} seconds; completion rates range from
{summary.task_completed.min():.1%} to {summary.task_completed.max():.1%}.
Mean ease ranges from {summary.perceived_ease.min():.2f} to {summary.perceived_ease.max():.2f}/7.
Differences in fitted behavioral features are expected by construction of K-Means.
Outcome differences are descriptive, not independent validation: the generator
already links outcomes and behaviors through continuous friction.

## Research implications and limitations

Longer sessions, repeated errors and hesitation could motivate reviewing recipient
entry, amount confirmation and transfer review in a real study. This dataset has
no step-level observations, so it cannot identify which screen causes friction.
Collect recordings, event timestamps and participant explanations before proposing
specific interface changes. Do not use these synthetic rates as product benchmarks.

Small simulated samples, assumed distributions, ordinal ease, count data,
outliers, feature weighting and K-Means geometry limit interpretation. There is no
resampling stability study, external validation, causal inference or population
generalization. Failed-session times represent time until stopping, not completion;
mixing them with completed-session durations can affect distance-based clustering.
"""
    (output / "report.md").write_text(report, encoding="utf-8")
    print(f"Synthetic sessions: {len(frame)}; selected K: {model.n_clusters}; silhouette: {best:.3f}")
    return frame, scores


if __name__ == "__main__":
    run_pipeline()
