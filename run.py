from problems.hj_1d import HJ1DProblem
from solvers.fd_baseline import solve
from metrics.l2_error import l2_error
from leaderboard import log_result

if __name__ == "__main__":
    # 1. Define problem
    problem = HJ1DProblem(grid_size=100)

    # 2. Call solver
    u_pred = solve(problem)

    # 3. Compute error
    error = l2_error(u_pred, problem.true_solution())

    # 4. Log result
    log_result("FD Baseline", error)
