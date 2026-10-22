# Synthetic Pix usability: exploratory findings

All 120 sessions are synthetic. No actual participants or transfers were observed.

## Overall indicators

- Completion rate: 86.7% (assistance allowed).
- Help-needed rate: 28.3%.
- Median observed task time: 114.1 seconds.
- Median completion time among completed sessions: 113.3 seconds.
- Mean perceived ease: 5.14/7.

## Clustering assessment

K=6 maximizes mean silhouette among K=2..6, with score 0.320.
The improvement over the runner-up is only 0.011.
The selected K is at the edge of the tested range;
it should not be treated as a globally optimal number of clusters.
Negative individual silhouettes: 1.7%.
These diagnostics do not provide convincing evidence of distinct user profiles.
This numerical optimum is only a descriptive partition of a continuous synthetic
distribution. It does not establish distinct behavioral profiles or validated personas.
Inspect k_comparison.csv, silhouette.png and clusters.png together; a 2D projection
does not prove separation. No score threshold alone establishes real user segments.

Cluster means, sizes, completion/help rates and perceived ease are in
cluster_indicators.csv; distributions are shown in cluster_indicators.png.
Partition sizes range from 9 to 30 sessions.
Mean observed task times range from 91.1 to
166.1 seconds; completion rates range from
66.7% to 100.0%.
Mean ease ranges from 4.70 to 5.68/7.
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
