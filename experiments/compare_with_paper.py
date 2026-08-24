import csv, os

def rows(path):
    with open(path,newline="") as f: return {r["algorithm"]:r for r in csv.DictReader(f)}

sim=rows("results/summary.csv")
paper=rows("results/paper_reported_metrics.csv")
print("algorithm,sim_utility,paper_utility,utility_diff,sim_regret,paper_regret,regret_diff")
for a in paper:
    if a not in sim: continue
    su=float(sim[a]["last50_mean_utility"]); pu=float(paper[a]["last50_mean_utility"])
    sr=float(sim[a]["cumulative_regret"]); pr=float(paper[a]["cumulative_regret"])
    print(f"{a},{su:.4f},{pu:.4f},{su-pu:+.4f},{sr:.2f},{pr:.2f},{sr-pr:+.2f}")
