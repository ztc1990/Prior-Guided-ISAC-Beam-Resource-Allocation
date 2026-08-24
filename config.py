from dataclasses import dataclass
import numpy as np

@dataclass
class Config:
    seed: int = 20260807
    n_slots: int = 600
    n_trials: int = 60
    n_beams: int = 32
    n_users: int = 4
    n_targets: int = 3
    angle_min: float = -60.0
    angle_max: float = 60.0
    resource_ratios: tuple = (0.35, 0.45, 0.55, 0.65, 0.75)
    lambda_comm: float = 0.62
    beta: float = 0.25
    gamma: float = 0.80
    candidate_L: int = 4
    prior_sigma_deg: float = 2.0
    motion_sigma_deg: float = 1.8
    sensing_motion_sigma_deg: float = 1.53
    blockage_prob: float = 0.045
    blockage_loss: float = 0.45
    switch_cost: float = 0.018
    reward_noise: float = 0.012

    @property
    def beam_angles(self):
        return np.linspace(self.angle_min, self.angle_max, self.n_beams)
