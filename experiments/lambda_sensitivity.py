import os,sys,csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import Config
from experiments.run_all import run_policy

def main():
    vals=[0.40,0.50,0.62,0.70,0.80]
    rows=[]
    for lam in vals:
        cfg=Config(lambda_comm=lam)
        rs=[]; gs=[]; hs=[]
        for k in range(cfg.n_trials):
            r,g,h=run_policy("Prior-Guided UCB",cfg,cfg.seed+1009*k)
            rs.append(r[-50:].mean()); gs.append(g.sum()); hs.append(h.mean()*100)
        rows.append([lam,np.mean(rs),np.mean(gs),np.mean(hs)])
    os.makedirs("results",exist_ok=True)
    with open("results/lambda_sensitivity.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["lambda","last50_mean_utility","cumulative_regret","beam_hit_rate_pct"]);w.writerows(rows)
    for r in rows: print(r)
if __name__=="__main__": main()
