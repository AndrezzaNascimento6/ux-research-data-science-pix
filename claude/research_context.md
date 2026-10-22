# Synthetic Pix usability research

All 120 sessions are synthetic; no people or real transfers were observed.
Results describe this simulation only and are exploratory, not product benchmarks.

## Objective and task

Explore behavioral variation and usability indicators during a Pix transfer:
recipient entry, amount entry, review and confirmation. Use the results to frame
questions for future real-participant research, not to establish personas.

## Method

- Fixed seed 42; continuous friction plus noise, without predefined groups.
  Poisson errors/hesitations, lognormal baseline time plus event delays,
  Bernoulli help/completion, and noisy rounded/clipped ease ratings.
- Pandas descriptive statistics and Spearman correlations; static visualizations.
- K-Means inputs: time, errors and hesitations, each transformed with `log1p`
  then standardized. Seed 42, `n_init=30`; K=2..6 compared by mean silhouette
  in the full feature space. Help, completion and ease are comparison indicators,
  not clustering inputs. PCA is visualization only.

## Exported results

K=6 has the highest silhouette: 0.319569, rounded to **0.320**. This does not
support clearly distinct profiles. The runner-up is K=3 (0.308113); the improvement
is only 0.011. K=6 is the upper boundary tested, not a proven global optimum.
Negative individual silhouettes: 1.7%. Cluster IDs are arbitrary labels.

Overall: completion 86.7% (assistance allowed), help 28.3%, median observed time
114.1 s, median time among completed sessions 113.3 s, mean ease 5.14/7.

`analysis_summary.csv` copies the six rows of `outputs/cluster_indicators.csv`,
renames columns for clarity and rounds indicators to three decimal places.
Counts are exact; no model is refitted. Rates are proportions (0–1), not percentages.
Time means include completed and stopped sessions; failed-session times are not
completion times. Errors and hesitations are mean counts; hesitation means a pause
of at least three seconds. Ease ranges from 1 (very difficult) to 7 (very easy).
Help means assistance was needed; completion does not imply unassisted success.

## Limits on interpretation

Small simulated sample; partitions contain 9–30 sessions. Behavioral differences
are expected because K-Means optimizes those same features. Outcome associations
partly reflect the generator's shared friction assumptions, not independent
validation. Means hide variation; ease is ordinal. Scaling, correlated inputs,
outliers, discrete counts and Euclidean geometry affect partitions. No resampling
stability, significance testing, causal inference or external validation exists.
There are no screen-level events, recordings, quotes or demographic data; specific
screen failures and explanations cannot be inferred.

Sources: `outputs/cluster_indicators.csv`, `outputs/k_comparison.csv`,
`outputs/report.md`; methodology and definitions: `README.md`.
