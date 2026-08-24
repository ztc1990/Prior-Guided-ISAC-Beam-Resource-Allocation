# GitHub upload checklist

1. Create a new public repository, for example `prior-guided-isac-beam-allocation`.
2. Upload the contents of this repository root (not the outer ZIP folder).
3. Keep `README.md`, `REPRODUCIBILITY_NOTE.md`, `requirements.txt`, and `LICENSE` at the repository root.
4. Confirm that GitHub displays `results/summary.csv` and `results/paper_reported_metrics.csv` separately.
5. Run locally from a clean environment:
   ```bash
   python -m pip install -r requirements.txt
   python experiments/run_all.py
   python experiments/lambda_sensitivity.py
   python experiments/make_figures.py
   python experiments/compare_with_paper.py
   ```
6. Commit the generated CSV and figures used for the revision.
7. Copy the public repository URL into the revised manuscript and point-by-point response.
8. Do not claim exact table reproduction until the legacy beta/gamma/L values and regret convention are confirmed.
