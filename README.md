# Prior-Guided ISAC Beam Selection and Resource Allocation

Reproducibility implementation for the manuscript **基于先验信息的通感一体化网络波束选择与资源分配策略研究**.

## Install
```bash
python -m pip install -r requirements.txt
```

## Reproduce
```bash
python experiments/run_all.py
python experiments/lambda_sensitivity.py
python experiments/make_figures.py
python experiments/compare_with_paper.py
```

The main simulator implements dynamic prior scoring, top-L candidate-beam screening, UCB exploration in the reduced action space, online feedback updates, and the four manuscript baselines.

### Important
Read `REPRODUCIBILITY_NOTE.md` before using the repository. The manuscript fixes the main scenario parameters and seed, but does not numerically state beta, gamma, or L. The code therefore distinguishes **simulated outputs** from the **paper-reported reference table** rather than hard-coding manuscript numbers into the simulator.

## Repository contents
- `config.py`: simulation configuration
- `environment.py`: mobile ISAC environment
- `algorithms/policies.py`: proposed policy and baselines
- `experiments/run_all.py`: 600-slot × 60-trial main experiment
- `experiments/lambda_sensitivity.py`: lambda sensitivity
- `experiments/make_figures.py`: figures
- `experiments/compare_with_paper.py`: transparent comparison to reported values
- `results/paper_reported_metrics.csv`: manuscript table transcription
- `REPRODUCIBILITY_NOTE.md`: reconstruction scope and limitations

## License
MIT.
