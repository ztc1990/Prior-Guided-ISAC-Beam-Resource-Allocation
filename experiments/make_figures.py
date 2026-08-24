import os, csv
import numpy as np
import matplotlib.pyplot as plt

def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def main():
    os.makedirs("figures", exist_ok=True)
    rows=load("results/summary.csv")
    alg=[r["algorithm"] for r in rows]
    util=[float(r["last50_mean_utility"]) for r in rows]
    regret=[float(r["cumulative_regret"]) for r in rows]
    hit=[float(r["beam_hit_rate_pct"]) for r in rows]

    for vals, ylabel, fn in [
        (util, "Last-50 mean utility", "summary_utility.png"),
        (regret, "Cumulative regret", "summary_regret.png"),
        (hit, "Beam hit rate (%)", "summary_hit_rate.png"),
    ]:
        plt.figure(figsize=(6.4,4.2))
        plt.bar(alg, vals)
        plt.ylabel(ylabel); plt.xticks(rotation=18, ha="right")
        plt.tight_layout(); plt.savefig("figures/"+fn, dpi=200); plt.close()

    sens=load("results/lambda_sensitivity.csv")
    x=[float(r["lambda"]) for r in sens]
    y=[float(r["last50_mean_utility"]) for r in sens]
    plt.figure(figsize=(6.4,4.2))
    plt.plot(x,y,marker="o"); plt.xlabel("Communication weight λ"); plt.ylabel("Last-50 mean utility")
    plt.tight_layout(); plt.savefig("figures/lambda_sensitivity.png",dpi=200); plt.close()

if __name__=="__main__": main()
