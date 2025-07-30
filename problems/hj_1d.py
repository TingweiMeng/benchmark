import numpy as np

class HJ1DProblem:
    def __init__(self, grid_size=100):
        self.grid_size = grid_size
        self.x = np.linspace(0, 1, grid_size)
        self.u0 = np.sin(2 * np.pi * self.x)  # Initial condition

    def true_solution(self):
        """Ground truth solution (for testing)"""
        return np.sin(2 * np.pi * self.x)  # Assume steady state for now
