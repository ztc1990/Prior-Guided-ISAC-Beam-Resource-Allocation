import numpy as np

class ISACEnvironment:
    def __init__(self, cfg, rng):
        self.cfg, self.rng = cfg, rng
        self.beams = cfg.beam_angles
        self.user_angles = rng.uniform(-45, 45, cfg.n_users)
        self.target_angles = rng.uniform(-45, 45, cfg.n_targets)
        self.prev_beam = None

    def advance(self):
        c = self.cfg
        self.user_angles = np.clip(
            self.user_angles + self.rng.normal(0, c.motion_sigma_deg, c.n_users),
            c.angle_min, c.angle_max)
        self.target_angles = np.clip(
            self.target_angles + self.rng.normal(0, c.sensing_motion_sigma_deg, c.n_targets),
            c.angle_min, c.angle_max)

    def prior_scores(self):
        c = self.cfg
        est_users = self.user_angles + self.rng.normal(0, c.prior_sigma_deg, c.n_users)
        est_targets = self.target_angles + self.rng.normal(0, c.prior_sigma_deg, c.n_targets)
        du = (self.beams[:,None] - est_users[None,:]) / 10.0
        dt = (self.beams[:,None] - est_targets[None,:]) / 9.0
        u = np.exp(-0.5*du*du).mean(axis=1)
        s = np.exp(-0.5*dt*dt).mean(axis=1)
        return 0.55*u + 0.45*s

    def deterministic_components_all(self):
        c = self.cfg
        du = (self.beams[:,None] - self.user_angles[None,:]) / 8.5
        dt = (self.beams[:,None] - self.target_angles[None,:]) / 7.5
        um = np.exp(-0.5*du*du).mean(axis=1)
        tm = np.exp(-0.5*dt*dt).mean(axis=1)
        snr = 0.25 + 8.0*um
        comm = np.log2(1.0+snr) / np.log2(9.25)
        return comm, tm

    def step(self, beam_idx, rho, lam):
        c = self.cfg
        comm_all, sense_all = self.deterministic_components_all()
        blocked = self.rng.random() < c.blockage_prob
        comm = comm_all[beam_idx] * ((1.0-c.blockage_loss) if blocked else 1.0)
        sensing = sense_all[beam_idx]
        sw = c.switch_cost if self.prev_beam is not None and beam_idx != self.prev_beam else 0.0
        r = lam*rho*comm + (1-lam)*(1-rho)*sensing - sw
        r += self.rng.normal(0, c.reward_noise)
        self.prev_beam = beam_idx
        self.advance()
        return float(r)

    def oracle(self, lam):
        c = self.cfg
        comm, sensing = self.deterministic_components_all()
        rho = np.asarray(c.resource_ratios)
        vals = lam*comm[:,None]*rho[None,:] + (1-lam)*sensing[:,None]*(1-rho[None,:])
        if self.prev_beam is not None:
            vals -= c.switch_cost
            vals[self.prev_beam,:] += c.switch_cost
        flat = int(np.argmax(vals))
        bi,ri = divmod(flat, len(rho))
        return float(vals[bi,ri]), bi, float(rho[ri])
