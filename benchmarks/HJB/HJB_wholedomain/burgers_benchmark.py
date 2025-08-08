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
# DOMAIN SETUP UTILITIES
# ==========================================

def setup_spatial_domain(dimension, domain_type='grid', **params):
    """Setup spatial domain for Burgers equation."""
    if domain_type == 'grid':
        if dimension == 1:
            nx = params.get('nx', 100)
            return np.linspace(0, 1, nx)
        
        elif dimension == 2:
            nx = params.get('nx', 50)
            ny = params.get('ny', 50)
            x = np.linspace(0, 1, nx)
            y = np.linspace(0, 1, ny)
            X, Y = np.meshgrid(x, y, indexing='ij')
            return np.stack([X, Y], axis=-1)
        
        else:
            raise NotImplementedError("Grid mode only supports 1D and 2D for Burgers")
    
    elif domain_type == 'points':
        n_points = params.get('n_points', 1000)
        np.random.seed(params.get('seed', 42))
        
        # For Burgers, focus on [0,1] in first coordinate, [-1,1] in others
        points = np.random.uniform(size=(n_points, dimension))
        points[:, 0] = points[:, 0]  # [0,1] for x-coordinate
        if dimension > 1:
            points[:, 1:] = 2 * points[:, 1:] - 1  # [-1,1] for other coordinates
        
        return points
    
    else:
        raise ValueError(f"Unknown domain_type: {domain_type}")

def compute_error_metrics(u_user, u_ref):
    """Comprehensive error analysis."""
    abs_error = np.abs(u_user - u_ref)
    
    l1_error = np.mean(abs_error)
    l2_error = np.sqrt(np.mean(abs_error**2))
    linf_error = np.max(abs_error)
    
    ref_norm = np.sqrt(np.mean(u_ref**2))
    rel_l2_error = l2_error / ref_norm if ref_norm > 1e-12 else l2_error
    
    return {
        'l1_error': l1_error,
        'l2_error': l2_error,
        'linf_error': linf_error,
        'relative_l2': rel_l2_error
    }

# ==========================================
# BENCHMARK RUNNER
# ==========================================

def run_test_case(dimension, domain_type, test_params=None):
    """Run a single test case."""
    if test_params is None:
        test_params = {'nu': 0.01}
    
    print(f"\nTest Case: {dimension}D, {domain_type} mode")
    print("-" * 30)
    
    # Setup domain
    spatial_points = setup_spatial_domain(dimension, domain_type, **test_params)
    time_points = np.linspace(0, 0.5, test_params.get('nt', 50))
    
    if hasattr(spatial_points, 'shape'):
        if spatial_points.ndim == 1:
            print(f"Spatial points: {len(spatial_points)}")
        else:
            print(f"Spatial points: {spatial_points.shape}")
    else:
        print(f"Spatial points: {len(spatial_points)}")
    print(f"Time points: {len(time_points)}")
    
    # Run user solver
    print("Running user solver...")
    user_start = time.time()
    try:
        u_user = solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **test_params)
        user_time = time.time() - user_start
        
        # Compute reference solution
        print("Computing reference solution...")
        u_ref = reference_solution(spatial_points, time_points, **test_params)
        
        # Validate shapes
        if u_user.shape != u_ref.shape:
            raise ValueError(f"Shape mismatch: user {u_user.shape} vs reference {u_ref.shape}")
        
        # Compute errors
        errors = compute_error_metrics(u_user, u_ref)
        
        # Results
        print(f"L1 Error: {errors['l1_error']:.2e}")
        print(f"L2 Error: {errors['l2_error']:.2e}")
        print(f"L∞ Error: {errors['linf_error']:.2e}")
        print(f"Relative L2: {errors['relative_l2']:.2e}")
        print(f"Solve time: {user_time:.4f}s")
        
        # Performance assessment
        if errors['l2_error'] < 1e-2:
            print("✓ Excellent accuracy!")
        elif errors['l2_error'] < 1e-1:
            print("✓ Good accuracy")
        else:
            print("⚠ Consider improving accuracy")
        
        return {
            'dimension': dimension,
            'domain_type': domain_type,
            'success': True,
            'user_time': user_time,
            'solution_user': u_user,
            'solution_ref': u_ref,
            'spatial_points': spatial_points,
            'time_points': time_points,
            **errors
        }
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return {
            'dimension': dimension,
            'domain_type': domain_type,
            'success': False,
            'error': str(e)
        }

def run_benchmark():
    """Run comprehensive Burgers benchmark."""
    print("Burgers Equation Benchmark")
    print("=" * 30)
    print("Problem: ∂u/∂t + u ∂u/∂x = ν ∂²u/∂x²")
    print("Initial: u(x,0) = -sin(πx)")
    
    # Define test cases
    test_cases = [
        (1, 'grid', {'nx': 100, 'nu': 0.01}),
        (2, 'grid', {'nx': 50, 'ny': 50, 'nu': 0.01}),
        (3, 'points', {'n_points': 1000, 'nu': 0.01}),
        (5, 'points', {'n_points': 1000, 'nu': 0.01}),
        (10, 'points', {'n_points': 1000, 'nu': 0.01}),
    ]
    
    results = []
    for dimension, domain_type, params in test_cases:
        result = run_test_case(dimension, domain_type, params)
        results.append(result)
    
    # Summary
    print(f"\n{'='*60}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*60}")
    print(f"{'Case':<15} {'Status':<10} {'L2 Error':<12} {'Time (s)':<10}")
    print("-" * 60)
    
    for result in results:
        case_name = f"{result['dimension']}D {result['domain_type']}"
        status = "✓ PASS" if result['success'] else "❌ FAIL"
        l2_error = f"{result.get('l2_error', 0):.2e}" if result['success'] else "N/A"
        time_str = f"{result.get('user_time', 0):.4f}" if result['success'] else "N/A"
        print(f"{case_name:<15} {status:<10} {l2_error:<12} {time_str:<10}")
    
    # Create visualizations
    create_visualization_suite(results)
    
    return results

def create_visualization_suite(results):
    """Create comprehensive visualizations."""
    successful_results = [r for r in results if r['success']]
    
    if not successful_results:
        print("No successful results to visualize.")
        return
    
    # 1D visualization
    result_1d = next((r for r in successful_results if r['dimension'] == 1), None)
    if result_1d:
        create_1d_visualization(result_1d)
    
    # 2D visualization  
    result_2d = next((r for r in successful_results if r['dimension'] == 2), None)
    if result_2d:
        create_2d_visualization(result_2d)
    
    # Scaling analysis
    create_scaling_analysis(successful_results)

def create_1d_visualization(result):
    """Create 1D-specific visualization."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    x = result['spatial_points']
    t = result['time_points']
    u_user = result['solution_user']
    u_ref = result['solution_ref']
    
    # Space-time plot - User
    im1 = axes[0,0].contourf(x, t, u_user.T, levels=20, cmap='viridis')
    axes[0,0].set_title('User Solution')
    axes[0,0].set_xlabel('x')
    axes[0,0].set_ylabel('t')
    plt.colorbar(im1, ax=axes[0,0])
    
    # Space-time plot - Reference
    im2 = axes[0,1].contourf(x, t, u_ref.T, levels=20, cmap='viridis')
    axes[0,1].set_title('Reference Solution')
    axes[0,1].set_xlabel('x')
    axes[0,1].set_ylabel('t')
    plt.colorbar(im2, ax=axes[0,1])
    
    # Error
    error = np.abs(u_user - u_ref)
    im3 = axes[1,0].contourf(x, t, error.T, levels=20, cmap='hot')
    axes[1,0].set_title(f'Absolute Error (max={np.max(error):.2e})')
    axes[1,0].set_xlabel('x')
    axes[1,0].set_ylabel('t')
    plt.colorbar(im3, ax=axes[1,0])
    
    # Time evolution
    time_indices = [0, len(t)//4, len(t)//2, 3*len(t)//4, -1]
    for i, ti in enumerate(time_indices):
        alpha = 0.5 + 0.5 * i / len(time_indices)
        axes[1,1].plot(x, u_ref[:, ti], '-', alpha=alpha, label=f't={t[ti]:.2f}')
        axes[1,1].plot(x, u_user[:, ti], '--', alpha=alpha)
    
    axes[1,1].set_xlabel('x')
    axes[1,1].set_ylabel('u(x,t)')
    axes[1,1].set_title('Time Evolution (solid=ref, dashed=user)')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('burgers_1d_results.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_2d_visualization(result):
    """Create 2D-specific visualization."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    u_user = result['solution_user']
    u_ref = result['solution_ref']
    
    # Final time solutions
    u_user_final = u_user[:, :, -1]
    u_ref_final = u_ref[:, :, -1]
    error_final = np.abs(u_user_final - u_ref_final)
    
    # User solution
    im1 = axes[0,0].contourf(u_user_final, levels=20, cmap='viridis')
    axes[0,0].set_title('User Solution (final)')
    plt.colorbar(im1, ax=axes[0,0])
    
    # Reference solution
    im2 = axes[0,1].contourf(u_ref_final, levels=20, cmap='viridis')
    axes[0,1].set_title('Reference Solution (final)')
    plt.colorbar(im2, ax=axes[0,1])
    
    # Error
    im3 = axes[0,2].contourf(error_final, levels=20, cmap='hot')
    axes[0,2].set_title('Absolute Error (final)')
    plt.colorbar(im3, ax=axes[0,2])
    
    # Cross-sections and error evolution
    mid_x = u_user_final.shape[0] // 2
    mid_y = u_user_final.shape[1] // 2
    
    axes[1,0].plot(u_ref_final[mid_x, :], label='Reference')
    axes[1,0].plot(u_user_final[mid_x, :], '--', label='User')
    axes[1,0].set_title('X cross-section')
    axes[1,0].legend()
    
    axes[1,1].plot(u_ref_final[:, mid_y], label='Reference')
    axes[1,1].plot(u_user_final[:, mid_y], '--', label='User')
    axes[1,1].set_title('Y cross-section')
    axes[1,1].legend()
    
    # Error evolution
    t = result['time_points']
    l2_errors = [np.sqrt(np.mean((u_user[:,:,i] - u_ref[:,:,i])**2)) for i in range(len(t))]
    axes[1,2].semilogy(t, l2_errors)
    axes[1,2].set_title('L2 Error Evolution')
    axes[1,2].set_xlabel('Time')
    axes[1,2].grid(True)
    
    plt.tight_layout()
    plt.savefig('burgers_2d_results.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_scaling_analysis(results):
    """Create scaling analysis across dimensions."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    dims = [r['dimension'] for r in results]
    l2_errors = [r['l2_error'] for r in results]
    times = [r['user_time'] for r in results]
    
    # Error scaling
    ax1.semilogy(dims, l2_errors, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Dimension')
    ax1.set_ylabel('L2 Error')
    ax1.set_title('Error vs Dimension')
    ax1.grid(True)
    
    # Time scaling
    ax2.semilogy(dims, times, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('Dimension')
    ax2.set_ylabel('Solve Time (seconds)')
    ax2.set_title('Performance vs Dimension')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('burgers_scaling_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Visualizations saved:")
    print("- burgers_1d_results.png")
    print("- burgers_2d_results.png") 
    print("- burgers_scaling_analysis.png")

if __name__ == "__main__":
    results = run_benchmark()
    print(f"\nBenchmark completed! Results: {len([r for r in results if r['success']])}/{len(results)} passed")
    
    # Save results
    import json
    results_clean = []
    for r in results:
        r_clean = {k: v for k, v in r.items() if k not in ['solution_user', 'solution_ref', 'spatial_points', 'time_points']}
        results_clean.append(r_clean)
    
    with open('burgers_benchmark_results.json', 'w') as f:
        json.dump(results_clean, f, indent=2)
    print("Results saved to 'burgers_benchmark_results.json'")