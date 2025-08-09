"""
HJB Benchmark Template - For Contributors
========================================
Use this template to create new HJB benchmarks.

Hierarchy: HJB Category -> Problem Type -> Specific Problem -> Test Cases
Example: HJB_wholedomain -> burgers -> burgers_sine_ic -> (1D, 2D, 3D, 5D, 10D)

Required solver interface:
    solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **params) -> solution
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from ..utils import *  # Import utility functions

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
YOUR_PROBLEM_NAME = "Your_HJB_Problem_Name"

def hamiltonian(p, **params):
    """
    Define your Hamiltonian H(p).
    
    Args:
        p: Momentum/gradient variable 
        **params: Problem-specific parameters
    
    Returns:
        Hamiltonian value H(p)
    """
    # TODO: Implement your Hamiltonian
    # Example: return 0.5 * np.sum(p**2, axis=-1) for Burgers
    raise NotImplementedError("Define your Hamiltonian function")

def initial_condition(spatial_points, **params):
    """
    Define your initial condition u(x, 0).
    
    Args:
        spatial_points: Spatial evaluation points
        **params: Additional parameters (ic_type, etc.)
    
    Returns:
        Initial condition values
    """
    # TODO: Implement your initial condition
    # Example: return -np.sin(np.pi * spatial_points) for Burgers
    raise NotImplementedError("Define your initial condition")

def reference_solution(spatial_points, time_points, **params):
    """
    Provide reference solution for validation.
    
    Args:
        spatial_points: Spatial evaluation points
        time_points: Time evaluation points  
        **params: Problem-specific parameters
    
    Returns:
        Reference solution for comparison
    """
    # TODO: Implement reference solution (analytical or high-accuracy numerical)
    raise NotImplementedError("Provide reference solution for validation")

# ==========================================
# TEST CONFIGURATION - CUSTOMIZE THESE
# ==========================================

def get_test_cases():
    """
    Define test cases for your problem.
    
    Returns:
        List of (dimension, test_params) tuples
    """
    # TODO: Define your test cases
    return [
        (1, {'nx': 100}),           # 1D with 100 points
        (2, {'nx': 50, 'ny': 50}),  # 2D with 50x50 grid
        (3, {'n_points': 1000}),    # 3D with 1000 random points
        (5, {'n_points': 1000}),    # 5D with 1000 random points
        (10, {'n_points': 1000}),   # 10D with 1000 random points
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