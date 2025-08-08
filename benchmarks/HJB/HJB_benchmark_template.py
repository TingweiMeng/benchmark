"""
HJB Benchmark Template - For Contributors
========================================
Use this template to create new HJB benchmarks.

Hierarchy: HJB Category -> Problem Type -> Specific Problem -> Test Cases
Example: HJB_wholedomain -> burgers -> burgers_sine_ic -> (1D_grid, 2D_grid, 3D_points, ...)

Required solver interface:
    solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **params) -> solution
    
    Solution format depends on domain_type:
    - 'grid': Returns array with shape matching spatial_points and time_points
    - 'points': Returns array with shape (n_points, n_times) or function callable
"""

import numpy as np
import matplotlib.pyplot as plt
import time

# ==========================================
# USER SOLVER IMPORT
# ==========================================
try:
    from solver import solve_HJB
except ImportError:
    print("Error: Please implement your solver in 'solver.py' with function 'solve_HJB'")
    print("Expected signature: solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **params)")
    exit(1)

# ==========================================
# PROBLEM DEFINITION - CUSTOMIZE THESE
# ==========================================

def hamiltonian(p, **params):
    """
    Define your Hamiltonian H(p).
    
    Args:
        p: Momentum/gradient variable (scalar or array)
        **params: Additional problem-specific parameters
    
    Returns:
        float or array: H(p)
    
    Example for Burgers: return 0.5 * p**2
    """
    # TODO: Implement your Hamiltonian
    raise NotImplementedError("Define your Hamiltonian function")

def initial_condition(spatial_points, ic_type='default', **params):
    """
    Define your initial condition u(x, 0).
    
    Args:
        spatial_points: Spatial evaluation points
        ic_type: Type of initial condition
        **params: Additional parameters
    
    Returns:
        array: u(x, 0) with appropriate shape
    
    Example for Burgers: return -np.sin(np.pi * spatial_points)
    """
    # TODO: Implement your initial condition(s)
    raise NotImplementedError("Define your initial condition")

def reference_solution(spatial_points, time_points, **params):
    """
    Provide reference solution for validation.
    
    Args:
        spatial_points: Spatial evaluation points
        time_points: Time evaluation points  
        **params: Problem-specific parameters
    
    Returns:
        array: Reference solution with appropriate shape
    
    Note: Leave empty in template, implement case by case with high-accuracy methods
    """
    # TODO: Implement reference solution (analytical or high-accuracy numerical)
    # This can be left empty in template and implemented per specific problem
    raise NotImplementedError("Provide reference solution for validation")

# ==========================================
# DOMAIN SETUP UTILITIES
# ==========================================

def setup_spatial_domain(dimension, domain_type='grid', **params):
    """
    Setup spatial domain for different dimensions and types.
    
    Args:
        dimension: Spatial dimension (1, 2, 3, ...)
        domain_type: 'grid' for structured grids, 'points' for arbitrary points
        **params: Domain parameters (nx, ny, ranges, n_points, etc.)
    """
    if domain_type == 'grid':
        if dimension == 1:
            nx = params.get('nx', 100)
            x_range = params.get('x_range', (0, 1))
            return np.linspace(x_range[0], x_range[1], nx)
        
        elif dimension == 2:
            nx = params.get('nx', 50)
            ny = params.get('ny', 50)
            x_range = params.get('x_range', (0, 1))
            y_range = params.get('y_range', (0, 1))
            x = np.linspace(x_range[0], x_range[1], nx)
            y = np.linspace(y_range[0], y_range[1], ny)
            X, Y = np.meshgrid(x, y, indexing='ij')
            return np.stack([X, Y], axis=-1)
        
        else:
            raise NotImplementedError("Grid mode only supports 1D and 2D")
    
    elif domain_type == 'points':
        n_points = params.get('n_points', 1000)
        domain_bounds = params.get('domain_bounds', [(0, 1)] * dimension)
        
        np.random.seed(params.get('seed', 42))
        points = np.random.uniform(
            low=[b[0] for b in domain_bounds],
            high=[b[1] for b in domain_bounds],
            size=(n_points, dimension)
        )
        return points
    
    else:
        raise ValueError(f"Unknown domain_type: {domain_type}")

def compute_error_metrics(u_user, u_ref):
    """Comprehensive error analysis."""
    abs_error = np.abs(u_user - u_ref)
    
    # Basic metrics
    l1_error = np.mean(abs_error)
    l2_error = np.sqrt(np.mean(abs_error**2))
    linf_error = np.max(abs_error)
    
    # Relative metrics
    ref_norm = np.sqrt(np.mean(u_ref**2))
    rel_l2_error = l2_error / ref_norm if ref_norm > 1e-12 else l2_error
    
    return {
        'l1_error': l1_error,
        'l2_error': l2_error,
        'linf_error': linf_error,
        'relative_l2': rel_l2_error
    }

# ==========================================
# BENCHMARK RUNNER - FOLLOW THIS STRUCTURE
# ==========================================

def run_test_case(dimension, domain_type, test_params=None):
    """
    Run a single test case.
    
    Args:
        dimension: Spatial dimension
        domain_type: 'grid' or 'points'
        test_params: Dict of test parameters
    """
    if test_params is None:
        test_params = {}
    
    print(f"\nTest Case: {dimension}D, {domain_type} mode")
    print("-" * 30)
    
    # Setup domain
    spatial_points = setup_spatial_domain(dimension, domain_type, **test_params)
    time_points = np.linspace(0, 0.5, test_params.get('nt', 50))
    
    print(f"Spatial points: {spatial_points.shape if hasattr(spatial_points, 'shape') else len(spatial_points)}")
    print(f"Time points: {len(time_points)}")
    
    # Run user solver
    print("Running user solver...")
    user_start = time.time()
    try:
        u_user = solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **test_params)
        user_time = time.time() - user_start
        
        # Compute reference solution
        u_ref = reference_solution(spatial_points, time_points, **test_params)
        
        # Compute errors
        errors = compute_error_metrics(u_user, u_ref)
        
        # Results
        print(f"L1 Error: {errors['l1_error']:.2e}")
        print(f"L2 Error: {errors['l2_error']:.2e}")
        print(f"L∞ Error: {errors['linf_error']:.2e}")
        print(f"Relative L2: {errors['relative_l2']:.2e}")
        print(f"Solve time: {user_time:.4f}s")
        
        return {
            'dimension': dimension,
            'domain_type': domain_type,
            'success': True,
            'user_time': user_time,
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
    """
    Run comprehensive benchmark across multiple test cases.
    """
    print("YOUR_PROBLEM_NAME Benchmark")
    print("=" * 40)
    
    # TODO: Define your test cases
    test_cases = [
        (1, 'grid', {'nx': 100}),
        (2, 'grid', {'nx': 50, 'ny': 50}),
        (3, 'points', {'n_points': 1000}),
        (5, 'points', {'n_points': 1000}),
        (10, 'points', {'n_points': 1000}),
    ]
    
    results = []
    for dimension, domain_type, params in test_cases:
        result = run_test_case(dimension, domain_type, params)
        results.append(result)
    
    # Summary
    print(f"\n{'='*50}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*50}")
    print(f"{'Case':<15} {'Status':<10} {'L2 Error':<12} {'Time (s)':<10}")
    print("-" * 50)
    
    for result in results:
        case_name = f"{result['dimension']}D {result['domain_type']}"
        status = "✓ PASS" if result['success'] else "❌ FAIL"
        l2_error = f"{result.get('l2_error', 0):.2e}" if result['success'] else "N/A"
        time_str = f"{result.get('user_time', 0):.4f}" if result['success'] else "N/A"
        print(f"{case_name:<15} {status:<10} {l2_error:<12} {time_str:<10}")
    
    # TODO: Create visualization
    create_visualization_suite(results)
    
    return results

def create_visualization_suite(results):
    """
    Create visualization adapted to the problem and results.
    TODO: Customize for your specific problem
    """
    # TODO: Implement problem-specific visualization
    pass

if __name__ == "__main__":
    results = run_benchmark()
    print(f"\nBenchmark completed! Results: {len([r for r in results if r['success']])}/{len(results)} passed")