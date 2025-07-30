import numpy as np

def l2_error(u_pred, u_true):
    """Compute L2 error"""
    return np.sqrt(np.mean((u_pred - u_true) ** 2))
