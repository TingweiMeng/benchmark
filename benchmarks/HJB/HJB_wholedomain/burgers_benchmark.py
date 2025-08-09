"""
Burgers Equation Benchmark
==========================
Benchmark for the viscous Burgers' equation using HJB formulation.

Hierarchy: HJB_wholedomain -> burgers -> burgers_sine_ic -> multiple test cases

Problem: ∂u/∂t + u ∂u/∂x = ν ∂²u/∂x² (1D case)
Domain: x ∈ [0, 1] with periodic boundary conditions
Initial condition: u(x, 0) = -sin(πx)

Test Cases:
- 1D grid: Traditional finite difference
- 2D grid: Burgers in first dimension, constant in second  
- High-D points: Point-wise evaluation for high-dimensional solvers

Required solver interface:
    solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, nu) -> solution
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.interpolate import RegularGridInterpolator

# ==========================================
# USER SOLVER IMPORT
# ==========================================
try:
    from solver import solve_HJB
except ImportError:
    print("Error: Please implement your solver in 'solver.py' with function 'solve_HJB'")
    print("Expected signature: solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, nu)")
    exit(1)

# ==========================================
# PROBLEM DEFINITION
# ==========================================

def hamiltonian(p, **params):
    """
    Hamiltonian for the Burgers' equation.
    H(p) = 0.5 * \|p\|_2^2
    
    Args:
        p: Momentum/gradient variable, np array with shape [n_pts, dim]
    
    Returns:
        array with size [n_pts]: H(p)
    """
    assert isinstance(p, np.ndarray) and p.ndim == 2, "Expected 2D array for momentum p in function hamiltonian"
    return 0.5 * np.sum(p**2, axis=-1)  # Sum over last dimension for multi-dimensional case

def initial_condition(spatial_points, ic_type='sine', **params):
    """
    Initial condition for the Burgers' equation.
    
    Args:
        spatial_points: Spatial evaluation points, np array with shape [n_pts, dim]
        ic_type: Type of initial condition ('sine', 'gaussian', 'shock')
            - 'sine': sum_{i=1}^n sin(πx_i) / n
            - 'gaussian': Gaussian whose mean and std are given by params
            - 'shock': Shock wave at x=0.5 (taking values -1 or 1), averaged over dimensions

    Returns:
        array: Initial condition values
    """
    assert isinstance(spatial_points, np.ndarray) and spatial_points.ndim == 2, "Expected 2D array for spatial_points in function initial_condition"
    
    if ic_type == 'sine':
        return -sum(np.sin(np.pi * spatial_points), axis=-1) / spatial_points.shape[-1]
    elif ic_type == 'gaussian':
        center = params.get('mean', 0.5)
        width = params.get('std', 0.1)
        return np.exp(-np.sum(((spatial_points - center) / width)**2, axis=-1) / 2) / (np.sqrt(2 * np.pi) * width)**spatial_points.shape[-1]
    elif ic_type == 'shock':
        return np.mean(np.where(spatial_points[:, 0] < 0.5, 1.0, -1.0), axis=-1)
    else:
        raise ValueError(f"Unknown initial condition type: {ic_type}")

# TODO: check ref solution
def reference_solution(spatial_points, time_points, nu=0.01, **params):
    """
    High-accuracy reference solution using fine grid finite differences.
    """
    # if spatial_points.ndim == 1:
    #     return reference_solution_1d(spatial_points, time_points, nu)
    # else:
    #     return reference_solution_multid(spatial_points, time_points, nu, **params)
    return 0* spatial_points[...,0]

# comment from here
def reference_solution_1d(x, t, nu):
    """1D reference solution with fine grid."""
    # Use 4x finer grid for higher accuracy
    x_fine = np.linspace(x[0], x[-1], 4*len(x))
    t_fine = np.linspace(t[0], t[-1], 4*len(t))
    
    nx, nt = len(x_fine), len(t_fine)
    dx, dt = x_fine[1] - x_fine[0], t_fine[1] - t_fine[0]
    
    # Stability check
    cfl = dt / dx
    diffusion_number = nu * dt / dx**2
    if cfl > 0.5 or diffusion_number > 0.5:
        print(f"Warning: Potentially unstable parameters (CFL={cfl:.3f}, DN={diffusion_number:.3f})")
    
    # Initialize solution
    u = np.zeros((nx, nt))
    u[:, 0] = initial_condition(x_fine)
    
    # Higher-order time stepping (RK2) with higher-order spatial discretization
    for n in range(nt - 1):
        # RK2 step 1
        k1 = compute_rhs(u[:, n], dx, nu)
        u_temp = u[:, n] + 0.5 * dt * k1
        
        # Apply periodic boundary conditions
        u_temp[0] = u_temp[-2]
        u_temp[-1] = u_temp[1]
        
        # RK2 step 2
        k2 = compute_rhs(u_temp, dx, nu)
        u[:, n + 1] = u[:, n] + dt * k2
        
        # Apply periodic boundary conditions
        u[0, n + 1] = u[-2, n + 1]
        u[-1, n + 1] = u[1, n + 1]
    
    # Interpolate back to original grid
    interp = RegularGridInterpolator((x_fine, t_fine), u, method='linear')
    X, T = np.meshgrid(x, t, indexing='ij')
    points = np.stack([X, T], axis=-1)
    return interp(points)

def compute_rhs(u, dx, nu):
    """Compute RHS of Burgers equation with higher-order schemes."""
    rhs = np.zeros_like(u)
    
    # Higher-order upwind for convection (3rd order)
    for i in range(2, len(u) - 2):
        if u[i] >= 0:
            # Backward difference (3rd order)
            dudx = (2*u[i+1] + 3*u[i] - 6*u[i-1] + u[i-2]) / (6*dx)
        else:
            # Forward difference (3rd order)  
            dudx = (-u[i+2] + 6*u[i+1] - 3*u[i] - 2*u[i-1]) / (6*dx)
        
        # Second derivative (central difference)
        d2udx2 = (u[i+1] - 2*u[i] + u[i-1]) / dx**2
        
        rhs[i] = -u[i] * dudx + nu * d2udx2
    
    # Boundary treatment (2nd order)
    for i in [0, 1, len(u)-2, len(u)-1]:
        dudx = (u[min(i+1, len(u)-1)] - u[max(i-1, 0)]) / (2*dx)
        d2udx2 = (u[min(i+1, len(u)-1)] - 2*u[i] + u[max(i-1, 0)]) / dx**2
        rhs[i] = -u[i] * dudx + nu * d2udx2
    
    return rhs

def reference_solution_multid(spatial_points, time_points, nu, **params):
    """Multi-dimensional reference: Burgers in first dimension, others constant."""
    if spatial_points.ndim == 3 and spatial_points.shape[-1] >= 2:
        # Extract unique coordinates for 2D grid case
        x_coords = np.unique(spatial_points[..., 0])
        y_coords = np.unique(spatial_points[..., 1])
        
        # Solve 1D Burgers along x for each y
        u_1d = reference_solution_1d(x_coords, time_points, nu)
        
        # Extend to 2D (constant in y direction)
        nx, ny, nt = len(x_coords), len(y_coords), len(time_points)
        u_2d = np.zeros((nx, ny, nt))
        for j in range(ny):
            u_2d[:, j, :] = u_1d
        
        return u_2d
    else:
        # Point-wise evaluation case
        n_points = spatial_points.shape[0]
        n_times = len(time_points)
        u_points = np.zeros((n_points, n_times))
        
        for i, point in enumerate(spatial_points):
            x_1d = np.array([point[0]])  # Use first coordinate
            u_1d_point = reference_solution_1d(x_1d, time_points, nu)
            u_points[i, :] = u_1d_point[0, :]
        
        return u_points
# uncomment

# ==========================================
# TEST CONFIGURATION - CUSTOMIZE THESE
# ==========================================

def get_test_cases():
    """
    Define test cases for your problem.
    
    Returns:
        List of (dimension, test_params) tuples
    """
    return [
        # first non-viscous case
        (1, {'nx': 100, 'nu': 0.0}),           # 1D with 100 points
        (2, {'nx': 50, 'ny': 50, 'nu': 0.0}),  # 2D with 50x50 grid
        (3, {'n_points': 1000, 'nu': 0.0}),    # 3D with 1000 random points
        (5, {'n_points': 1000, 'nu': 0.0}),    # 5D with 1000 random points
        (10, {'n_points': 1000, 'nu': 0.0}),   # 10D with 1000 random points
        # then viscous case
        (1, {'nx': 100, 'nu': 0.01}),           # 1D with 100 points
        (2, {'nx': 50, 'ny': 50, 'nu': 0.01}),  # 2D with 50x50 grid
        (3, {'n_points': 1000, 'nu': 0.01}),    # 3D with 1000 random points
        (5, {'n_points': 1000, 'nu': 0.01}),    # 5D with 1000 random points
        (10, {'n_points': 1000, 'nu': 0.01}),   # 10D with 1000 random points
    ]

def get_default_params():
    """
    Define default problem parameters.
    
    Returns:
        Dict of default parameters
    """
    # TODO: Set your default parameters
    return {
        'time_final': 0.5,
        'nt': 50,
        # Add problem-specific parameters
    }

# ==========================================
# BENCHMARK RUNNER - STANDARD STRUCTURE
# ==========================================

def run_test_case(dimension, test_params):
    """Run a single test case."""
    print(f"\nTest Case: {dimension}D")
    print("-" * 20)
    
    # Merge with default parameters
    params = {**get_default_params(), **test_params}
    
    # Setup spatial domain
    spatial_points = setup_spatial_domain(dimension, **params)
    time_points = setup_time_domain(**params)
    
    print(f"Spatial points: {get_points_info(spatial_points)}")
    print(f"Time points: {len(time_points)}")
    
    # Run user solver
    print("Running user solver...")
    user_start = time.time()
    try:
        u_user = solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **params)
        user_time = time.time() - user_start
        
        # Compute reference solution
        print("Computing reference solution...")
        u_ref = reference_solution(spatial_points, time_points, **params)
        
        # Validate and compute errors
        validate_solution_shape(u_user, u_ref, spatial_points, time_points)
        errors = compute_error_metrics(u_user, u_ref)
        
        # Results
        print_results(errors, user_time)
        
        return {
            'dimension': dimension,
            'success': True,
            'user_time': user_time,
            'spatial_points': spatial_points,
            'time_points': time_points,
            'solution_user': u_user,
            'solution_ref': u_ref,
            **errors
        }
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return {
            'dimension': dimension,
            'success': False,
            'error': str(e)
        }

def run_benchmark():
    """Run comprehensive benchmark across all test cases."""
    print(f"{YOUR_PROBLEM_NAME} Benchmark")
    print("=" * 40)
    
    test_cases = get_test_cases()
    results = []
    
    for dimension, test_params in test_cases:
        result = run_test_case(dimension, test_params)
        results.append(result)
    
    # Print summary and create visualizations
    print_benchmark_summary(results)
    create_visualizations(results)
    
    return results

def create_visualizations(results):
    """
    Create problem-specific visualizations.
    TODO: Customize for your problem
    """
    successful_results = [r for r in results if r['success']]
    
    if not successful_results:
        return
    
    # TODO: Implement your visualizations
    # Use utility functions: plot_1d_results, plot_2d_results, plot_scaling_analysis
    print("TODO: Implement problem-specific visualizations")

if __name__ == "__main__":
    results = run_benchmark()
    save_results(results, f'{YOUR_PROBLEM_NAME}_benchmark_results.json')