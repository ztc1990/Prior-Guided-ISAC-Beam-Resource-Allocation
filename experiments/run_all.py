import os, sys, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import Config
from environment import ISACEnvironment
from algorithms.policies import PriorGuidedUCB, VanillaUCB, RandomPolicy, StaticPriorGreedy, TraditionalScan

def run_policy(name,cfg,seed):
    rng=np.random.default_rng(seed)
    env=ISACEnvironment(cfg,rng)
    initial_prior=env.prior_scores()
    if name=="Prior-Guided UCB": pol=PriorGuidedUCB(cfg)
    elif name=="UCB": pol=VanillaUCB(cfg)
    elif name=="Static-Prior Greedy": pol=StaticPriorGreedy(cfg,initial_prior)
    elif name=="Traditional Scan": pol=TraditionalScan(cfg)
    else: pol=RandomPolicy(cfg,rng)
    rewards=[]; regrets=[]; hits=[]
    for t in range(cfg.n_slots):
        prior=env.prior_scores()
        oracle, obi, _ = env.oracle(cfg.lambda_comm)
        bi,ri=pol.choose(t,prior)
        rho=cfg.resource_ratios[ri]
        r=env.step(bi,rho,cfg.lambda_comm)
        pol.update(bi,ri,r)
        rewards.append(r); regrets.append(max(0.0,oracle-r))
        hits.append(abs(int(bi)-int(obi))<=1)
    return np.asarray(rewards),np.asarray(regrets),np.asarray(hits)

def aggregate(name,cfg):
    rr=[]; rg=[]; hh=[]
    for k in range(cfg.n_trials):
        r,g,h=run_policy(name,cfg,cfg.seed+1009*k)
        rr.append(r); rg.append(g); hh.append(h)
    rr=np.asarray(rr); rg=np.asarray(rg); hh=np.asarray(hh)
    return float(rr[:,-50:].mean()), float(rg.sum(1).mean()), float(100*hh.mean())

def main():
    cfg=Config()
    names=["Random","Traditional Scan","UCB","Static-Prior Greedy","Prior-Guided UCB"]
    os.makedirs("results",exist_ok=True)
    rows=[[name,*aggregate(name,cfg)] for name in names]
    with open("results/summary.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["algorithm","last50_mean_utility","cumulative_regret","beam_hit_rate_pct"]); w.writerows(rows)
    print("algorithm,last50_mean_utility,cumulative_regret,beam_hit_rate_pct")
    for x in rows: print(f"{x[0]},{x[1]:.4f},{x[2]:.3f},{x[3]:.2f}")
if __name__=="__main__": main()
