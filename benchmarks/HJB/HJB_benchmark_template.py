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


# ==========================================
# METADATA EXTRACTION - FOR WEBSITE
# ==========================================
def get_benchmark_metadata():
    """
    Extract benchmark metadata for website display.
    This function is automatically inherited by all benchmarks.
    Override get_problem_specific_info() to customize.
    """
    test_cases = get_test_cases()
    
    # Extract parameter variations automatically
    dimensions = sorted(list(set(case[0] for case in test_cases)))
    
    # Detect parameter types automatically
    all_params = {}
    for _, params in test_cases:
        for key, value in params.items():
            if key not in all_params:
                all_params[key] = set()
            all_params[key].add(value)
    
    # Convert sets to sorted lists
    parameter_variations = {k: sorted(list(v)) for k, v in all_params.items()}
    
    # Auto-detect point generation methods
    grid_cases = []
    random_cases = []
    for dim, params in test_cases:
        if 'nx' in params or 'ny' in params or 'nz' in params:
            grid_cases.append(dim)
        else:
            random_cases.append(dim)
    
    # Get problem-specific info (users override this)
    problem_info = get_problem_specific_info()
    
    return {
        "name": problem_info.get("name", YOUR_PROBLEM_NAME.replace("_", " ")),
        "category": problem_info.get("category", "HJB"),
        "short_description": problem_info.get("short_description", "PDE benchmark problem"),
        "equation": problem_info.get("equation", "Fill in equation"),
        "initial_condition": problem_info.get("initial_condition", "Fill in initial condition"),
        "file_path": f"{YOUR_PROBLEM_NAME.lower()}_benchmark.py",
        
        # Auto-generated stats
        "quick_stats": {
            "total_cases": len(test_cases),
            "dimension_range": f"1D-{max(dimensions)}D" if len(dimensions) > 1 else f"{dimensions[0]}D",
            "point_types": get_point_types(grid_cases, random_cases),
            "parameter_count": len(parameter_variations)
        },
        
        # Auto-generated test case details
        "test_cases": [
            {
                "case_id": i+1,
                "dimension": case[0],
                "parameters": case[1],
                "point_type": "Grid" if case[0] in grid_cases else "Random",
                "point_details": get_point_details(case[0], case[1]),
                "physics_regime": get_physics_regime(case[1]),
                "description": get_case_description(case[0], case[1], problem_info)
            }
            for i, case in enumerate(test_cases)
        ],
        
        # Auto-generated parameter variations
        "parameter_variations": {
            "dimensions": dimensions,
            "grid_dimensions": sorted(list(set(grid_cases))),
            "random_dimensions": sorted(list(set(random_cases))),
            **parameter_variations
        },
        
        # Testing aspects (auto-generated with fallbacks)
        "testing_aspects": get_testing_aspects(dimensions, parameter_variations, problem_info)
    }

def get_problem_specific_info():
    """
    Override this function in your specific benchmark to provide custom info.
    Default implementation provides generic information.
    """
    return {
        "name": YOUR_PROBLEM_NAME.replace("_", " "),
        "category": "HJB", 
        "short_description": "PDE benchmark problem",
        "equation": "Please specify the equation in get_problem_specific_info()",
        "initial_condition": "Please specify initial condition in get_problem_specific_info()"
    }

def get_point_details(dimension, params):
    """Auto-detect point generation details."""
    if 'nx' in params and 'ny' in params and 'nz' in params:
        return f"{params['nx']}×{params['ny']}×{params['nz']} grid"
    elif 'nx' in params and 'ny' in params:
        return f"{params['nx']}×{params['ny']} grid"
    elif 'nx' in params:
        return f"{params['nx']} grid points"
    elif 'n_points' in params:
        return f"{params['n_points']} random points"
    else:
        return "Custom point distribution"

def get_physics_regime(params):
    """Auto-detect physics regime - override for problem-specific logic."""
    if 'nu' in params:
        nu = params['nu']
        if nu == 0.0:
            return "Inviscid"
        elif nu <= 0.01:
            return "Viscous"
        else:
            return "Highly Viscous"
    return "Standard"

def get_case_description(dimension, params, problem_info):
    """Generate case description - override for problem-specific logic."""
    regime = get_physics_regime(params)
    return f"{dimension}D {regime.lower()} case"

def get_point_types(grid_cases, random_cases):
    """Auto-detect point generation types."""
    types = []
    if grid_cases:
        types.append("Grid")
    if random_cases:
        types.append("Random")
    return types

def get_testing_aspects(dimensions, parameter_variations, problem_info):
    """Auto-generate testing aspects."""
    aspects = {}
    
    if len(dimensions) > 1:
        aspects["dimensional_scaling"] = f"Tests solver performance from {min(dimensions)}D to {max(dimensions)}D"
    
    if 'nu' in parameter_variations:
        nu_values = parameter_variations['nu']
        if 0.0 in nu_values:
            aspects["physics_regimes"] = "Tests both inviscid and viscous regimes"
        else:
            aspects["physics_regimes"] = f"Tests viscous behavior with ν = {nu_values}"
    
    # Add more auto-detection logic as needed
    
    return aspects

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    results = run_benchmark()
    save_results(results, f'{YOUR_PROBLEM_NAME}_benchmark_results.json')