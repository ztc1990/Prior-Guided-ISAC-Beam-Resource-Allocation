# Reproducibility note

This repository is a reconstruction from the revised manuscript and is intended to make the disclosed simulation logic executable.

## Parameters explicitly fixed by the manuscript
- 32 beams spanning -60 to 60 degrees
- 4 communication users and 3 sensing targets
- communication-resource ratios: 0.35, 0.45, 0.55, 0.65, 0.75
- 600 slots, 60 independent trials
- random seed: 20260807
- communication weight lambda: 0.62
- baselines: random, traditional scan, no-prior UCB, static-prior greedy

## Legacy parameters not numerically specified in the manuscript
The revised manuscript defines the exploration coefficient beta, prior coefficient gamma, and top-L candidate-set size, but does not provide their numerical values in Table 1. The original standalone Python source could not be recovered from the archived project files.

Therefore `config.py` contains explicit **reconstruction defaults**, not a claim that these were the historical values used to produce the manuscript table.

`results/paper_reported_metrics.csv` is a transcription of the manuscript table for comparison only. It is never read by the simulator to generate results.

Run:
```bash
python experiments/run_all.py
python experiments/compare_with_paper.py
```

For a strict archival reproduction of the manuscript's exact numerical table, replace the reconstruction-only parameters with the values from the original experiment source if/when that source is recovered, then regenerate `results/summary.csv`.
