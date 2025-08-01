import numpy as np

def burgers_hamiltonian(p):
    """
    Hamiltonian for the Burgers' equation.
    H(p) = 0.5 * p^2
    """
    return 0.5 * p**2

def burgers_initial_condition(x):
    """
    Initial condition for the Burgers' equation.
    u(x, 0) = -sin(pi * x)
    """
    return -np.sin(np.pi * x)

def burgers_reference_solution(x, t, nu):
    """
    Reference solution for the Burgers' equation using a simple finite difference method.
    """
    nx = len(x)
    nt = len(t)
    dx = x[1] - x[0]
    dt = t[1] - t[0]

    # Initialize solution array
    u = np.zeros((nx, nt))
    u[:, 0] = burgers_initial_condition(x)  # Initial condition

    # Time-stepping loop
    for n in range(0, nt - 1):
        u[1:-1, n + 1] = (
            u[1:-1, n]
            - dt / (2 * dx) * u[1:-1, n] * (u[2:, n] - u[:-2, n])
            + nu * dt / dx**2 * (u[2:, n] - 2 * u[1:-1, n] + u[:-2, n])
        )
        # Periodic boundary conditions
        u[0, n + 1] = u[-2, n + 1]
        u[-1, n + 1] = u[1, n + 1]

    return u

def test_solver(solver):
    """
    Test script for the Burgers' equation benchmark.

    Args:
        solver (function): User's solver function. Must take (Hamiltonian, initial_condition, x, t, nu)
                           and return the solution u(x, t).

    Returns:
        float: L2 error between the user's solution and the reference solution.
    """
    # Define benchmark parameters
    x = np.linspace(0, 1, 100)  # Spatial points
    t = np.linspace(0, 0.5, 50)  # Time points
    nu = 0.01  # Viscosity coefficient

    # Compute reference solution
    reference_u = burgers_reference_solution(x, t, nu)

    # Compute user's solution
    user_u = solver(burgers_hamiltonian, burgers_initial_condition, x, t, nu)

    # Compute L2 error
    error = np.sqrt(np.sum((user_u - reference_u) ** 2) / np.sum(reference_u**2))
    print(f"L2 Error: {error}")
    return error