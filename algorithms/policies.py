import numpy as np

class PriorGuidedUCB:
    def __init__(self, cfg):
        self.c=cfg
        self.R=len(cfg.resource_ratios)
        A=cfg.n_beams*self.R
        self.n=np.zeros(A); self.m=np.zeros(A)
    def choose(self,t,prior):
        c=self.c
        cand=np.argpartition(prior, -c.candidate_L)[-c.candidate_L:]
        ids=(cand[:,None]*self.R + np.arange(self.R)[None,:]).ravel()
        score=self.m[ids]+c.beta*np.sqrt(np.log(t+2)/(self.n[ids]+1))
        score += c.gamma*np.repeat(prior[cand], self.R)
        a=int(ids[np.argmax(score)])
        return a//self.R, a%self.R
    def update(self,bi,ri,r):
        a=bi*self.R+ri
        self.n[a]+=1
        self.m[a]+=(r-self.m[a])/self.n[a]

class VanillaUCB(PriorGuidedUCB):
    def choose(self,t,prior=None):
        ids=np.arange(len(self.n))
        score=self.m+self.c.beta*np.sqrt(np.log(t+2)/(self.n+1))
        a=int(np.argmax(score))
        return a//self.R, a%self.R

class StaticPriorGreedy:
    def __init__(self,cfg,initial_prior):
        self.c=cfg
        self.initial_prior=np.asarray(initial_prior)
    def choose(self,t,prior=None):
        bi=int(np.argmax(self.initial_prior))
        # static rule: fixed mid communication allocation
        ri=len(self.c.resource_ratios)//2
        return bi,ri
    def update(self,*args): pass

class RandomPolicy:
    def __init__(self,c,rng): self.c,self.rng=c,rng
    def choose(self,t,prior=None):
        return int(self.rng.integers(self.c.n_beams)), int(self.rng.integers(len(self.c.resource_ratios)))
    def update(self,*args): pass

class TraditionalScan:
    def __init__(self,cfg):
        self.c=cfg
    def choose(self,t,prior=None):
        # periodic exhaustive sweep proxy: cycle beams, fixed middle resource split
        bi=t % self.c.n_beams
        ri=len(self.c.resource_ratios)//2
        return bi,ri
    def update(self,*args): pass
