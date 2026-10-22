# Interpretation task

Act as a Senior UX Researcher. Use only the attached `research_context.md` and
`analysis_summary.csv`. All sessions are synthetic; interpretations are exploratory.
Silhouette 0.320 does not support clearly distinct user profiles.

Return a concise English response (maximum 450 words):

1. Evidence: up to three descriptive comparisons, citing cluster IDs, sample sizes
   and supplied metrics. Call them exploratory partitions, not personas or types.
2. Hypotheses: up to three possible explanations of difficulty during the Pix
   journey. Label each as untested; link it to a cited observation, state what is
   unknown, and suggest what evidence could distinguish competing explanations.
   Screen-specific mechanisms may be proposed only as hypotheses, never findings.
3. Future research: propose focused questions and methods to test those hypotheses
   with real participants (e.g., step timestamps, observation, intervention logs,
   follow-up questions). Do not present interface changes as validated solutions.
4. Limits: briefly explain weak separation, synthetic generation and the absence
   of causal or population-level evidence.

Do not invent metrics, quotes, demographics, significance, causality or new
clusters. Do not claim that 100% completion implies no difficulty or no help.
Use rates as proportions or convert explicitly to percentages; ease is 1–7.
Separate observations from hypotheses. If evidence is insufficient, say so.
Do not browse, request raw sessions, run code or refit the model.

## Manual use

In one new Claude conversation, attach only `research_context.md` and
`analysis_summary.csv`, then paste the task above (omit this section). If file
attachment is unavailable, paste both files once after the task, with filenames
as delimiters. The context is self-contained; do not attach plots, raw data,
source code or the full README. The response length limit reduces output usage.
