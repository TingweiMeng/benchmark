"""
Stochastic Linear Quadratic Regulator (SLQR) Benchmark
=======================================================
Benchmark for the stochastic LQR problem via the viscous HJB equation.

Problem: Minimize E[∫₀ᵀ ½|u|² dt + ½|x(T)|²]
Dynamics: dx = u dt + σ dW  (controlled diffusion)

HJB equation (time-reversed, τ = T - t):
    ∂φ/∂τ + ½|∇φ|² - ½σ²Δφ = 0,   φ(x, 0) = ½|x|²

Analytical solution (d = dimension):
    φ(x, τ) = ½|x|² / (1 + τ)  +  ½σ²d · ln(1 + τ)

Verification:
    ∂φ/∂τ = -½|x|²/(1+τ)² + ½σ²d/(1+τ)
    ½|∇φ|² = ½|x|²/(1+τ)²
    ½σ²Δφ  = ½σ²d/(1+τ)
    Sum: 0  ✓

Test Cases: 1D–10D, σ ∈ {0.1, 0.5} to probe diffusion effects.

Required solver interface:
    solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, sigma=σ) -> solution
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from ...utils import *

try:
    from solver import solve_HJB
except ImportError:
    print("Error: Please implement your solver in 'solver.py' with function 'solve_HJB'")
    exit(1)

# ==========================================
# PROBLEM DEFINITION
# ==========================================
YOUR_PROBLEM_NAME = "Stochastic_LQR"


def hamiltonian(p, **params):
    """
    Hamiltonian for stochastic LQR: H(p) = ½|p|².
    The diffusion term -½σ²Δφ is handled separately by the solver via sigma param.

    Args:
        p: Costate variable, shape [n_pts, dim]
    Returns:
        H(p), shape [n_pts]
    """
    assert isinstance(p, np.ndarray) and p.ndim == 2
    return 0.5 * np.sum(p**2, axis=-1)


def initial_condition(spatial_points, **params):
    """
    Terminal cost φ(x, 0) = ½|x|².

    Args:
        spatial_points: shape [n_pts, dim]
    Returns:
        φ(x, 0), shape [n_pts]
    """
    assert isinstance(spatial_points, np.ndarray) and spatial_points.ndim == 2
    return 0.5 * np.sum(spatial_points**2, axis=-1)


def reference_solution(spatial_points, time_points, **params):
    """
    Analytical solution: φ(x, τ) = ½|x|²/(1+τ) + ½σ²d·ln(1+τ).
    """
    sigma = params.get('sigma', 0.1)
    if spatial_points.ndim == 1:
        return _reference_1d(spatial_points, time_points, sigma)
    elif spatial_points.ndim == 3:
        return _reference_2d_grid(spatial_points, time_points, sigma)
    else:
        return _reference_points(spatial_points, time_points, sigma)


def _reference_1d(x, t, sigma):
    dim = 1
    x2 = x**2
    u = np.zeros((len(x), len(t)))
    for k, tau in enumerate(t):
        u[:, k] = 0.5 * x2 / (1.0 + tau) + 0.5 * sigma**2 * dim * np.log(1.0 + tau + 1e-15)
    return u


def _reference_2d_grid(spatial_points, t, sigma):
    dim = 2
    nx, ny, _ = spatial_points.shape
    x2 = np.sum(spatial_points**2, axis=-1)
    u = np.zeros((nx, ny, len(t)))
    for k, tau in enumerate(t):
        u[:, :, k] = 0.5 * x2 / (1.0 + tau) + 0.5 * sigma**2 * dim * np.log(1.0 + tau + 1e-15)
    return u


def _reference_points(spatial_points, t, sigma):
    n_pts, dim = spatial_points.shape
    x2 = np.sum(spatial_points**2, axis=-1)
    u = np.zeros((n_pts, len(t)))
    for k, tau in enumerate(t):
        u[:, k] = 0.5 * x2 / (1.0 + tau) + 0.5 * sigma**2 * dim * np.log(1.0 + tau + 1e-15)
    return u


# ==========================================
# TEST CONFIGURATION
# ==========================================

def get_test_cases():
    return [
        # Low noise
        (1,  {'nx': 100,            'domain_type': 'grid',   'sigma': 0.1}),
        (2,  {'nx': 50, 'ny': 50,  'domain_type': 'grid',   'sigma': 0.1}),
        (3,  {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.1}),
        (5,  {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.1}),
        (10, {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.1}),
        # High noise
        (1,  {'nx': 100,            'domain_type': 'grid',   'sigma': 0.5}),
        (2,  {'nx': 50, 'ny': 50,  'domain_type': 'grid',   'sigma': 0.5}),
        (3,  {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.5}),
        (5,  {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.5}),
        (10, {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.5}),
    ]


def get_default_params():
    return {
        'time_final': 1.0,
        'nt': 50,
        'x_range': (-2, 2),
        'y_range': (-2, 2),
        'sigma': 0.1,
    }


# ==========================================
# BENCHMARK RUNNER
# ==========================================

def run_test_case(dimension, test_params):
    print(f"\nTest Case: {dimension}D, σ={test_params.get('sigma', 0.1)}")
    print("-" * 20)

    params = {**get_default_params(), **test_params}
    params['domain_bounds'] = [(-2, 2)] * dimension

    spatial_points = setup_spatial_domain(dimension, **params)
    time_points = setup_time_domain(**params)

    print(f"Spatial points: {get_points_info(spatial_points)}")
    print(f"Time points: {len(time_points)}")

    print("Running user solver...")
    user_start = time.time()
    try:
        u_user = solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **params)
        user_time = time.time() - user_start

        print("Computing reference solution...")
        u_ref = reference_solution(spatial_points, time_points, **params)

        validate_solution_shape(u_user, u_ref, spatial_points, time_points)
        errors = compute_error_metrics(u_user, u_ref)
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
        return {'dimension': dimension, 'success': False, 'error': str(e)}


def run_benchmark():
    print(f"{YOUR_PROBLEM_NAME} Benchmark")
    print("=" * 40)

    results = [run_test_case(dim, params) for dim, params in get_test_cases()]
    print_benchmark_summary(results)
    create_visualizations(results)
    return results


def create_visualizations(results):
    """Visualize SLQR benchmark results."""
    successful = [r for r in results if r['success']]
    if not successful:
        return

    for i, result in enumerate(successful):
        dim = result['dimension']
        if dim == 1:
            plot_1d_results(result, filename=f'slqr_1d_case{i+1}.png')
        elif dim == 2:
            plot_2d_results(result, filename=f'slqr_2d_case{i+1}.png')

    plot_scaling_analysis(successful, filename='slqr_scaling_analysis.png')


# ==========================================
# METADATA EXTRACTION
# ==========================================

def get_benchmark_metadata():
    test_cases = get_test_cases()
    dimensions = sorted(set(c[0] for c in test_cases))
    all_params = {}
    for _, p in test_cases:
        for k, v in p.items():
            all_params.setdefault(k, set()).add(v)
    parameter_variations = {k: sorted(v, key=str) for k, v in all_params.items()}

    grid_cases = [d for d, p in test_cases if 'nx' in p or 'ny' in p]
    random_cases = [d for d, p in test_cases if 'n_points' in p]
    problem_info = get_problem_specific_info()

    return {
        "name": problem_info["name"],
        "category": problem_info["category"],
        "short_description": problem_info["short_description"],
        "equation": problem_info["equation"],
        "initial_condition": problem_info["initial_condition"],
        "file_path": f"{YOUR_PROBLEM_NAME.lower()}_benchmark.py",
        "quick_stats": {
            "total_cases": len(test_cases),
            "dimension_range": f"1D-{max(dimensions)}D",
            "point_types": get_point_types(grid_cases, random_cases),
            "parameter_count": len(parameter_variations),
        },
        "test_cases": [
            {
                "case_id": i + 1,
                "dimension": case[0],
                "parameters": case[1],
                "point_type": "Grid" if case[0] in grid_cases else "Random",
                "point_details": get_point_details(case[0], case[1]),
                "physics_regime": get_physics_regime(case[1]),
                "description": get_case_description(case[0], case[1], problem_info),
            }
            for i, case in enumerate(test_cases)
        ],
        "parameter_variations": {
            "dimensions": dimensions,
            "grid_dimensions": sorted(set(grid_cases)),
            "random_dimensions": sorted(set(random_cases)),
            **parameter_variations,
        },
        "testing_aspects": get_testing_aspects(dimensions, parameter_variations, problem_info),
    }


def get_problem_specific_info():
    return {
        "name": "Stochastic LQR",
        "category": "SOC",
        "short_description": "Viscous HJB equation for the stochastic LQR problem with Brownian noise",
        "equation": "∂φ/∂τ + ½|∇φ|² - ½σ²Δφ = 0",
        "initial_condition": "φ(x, 0) = ½|x|²",
        "background": "Stochastic LQR: dx = u dt + σ dW, minimizes E[∫½|u|²dt + ½|x(T)|²]",
        "applications": ["Stochastic control", "Risk-sensitive planning", "Diffusion model training"],
    }


def get_physics_regime(params):
    sigma = params.get('sigma', 0.1)
    if sigma <= 0.1:
        return "Low Noise"
    elif sigma <= 0.5:
        return "Moderate Noise"
    else:
        return "High Noise"


def get_case_description(dimension, params, problem_info):
    sigma = params.get('sigma', 0.1)
    pt = "grid" if 'nx' in params else "random points"
    return f"{dimension}D SLQR, σ={sigma} ({pt})"


def get_point_details(dimension, params):
    if 'nx' in params and 'ny' in params:
        return f"{params['nx']}×{params['ny']} grid"
    elif 'nx' in params:
        return f"{params['nx']} grid points"
    elif 'n_points' in params:
        return f"{params['n_points']} random points"
    return "Custom"


def get_point_types(grid_cases, random_cases):
    types = []
    if grid_cases:
        types.append("Grid")
    if random_cases:
        types.append("Random")
    return types


def get_testing_aspects(dimensions, parameter_variations, problem_info):
    aspects = {}
    if len(dimensions) > 1:
        aspects["dimensional_scaling"] = (
            f"Tests solver scalability from {min(dimensions)}D to {max(dimensions)}D"
        )
    if 'sigma' in parameter_variations:
        aspects["noise_sensitivity"] = (
            f"Tests behavior across noise levels σ ∈ {parameter_variations['sigma']}"
        )
    aspects["analytical_reference"] = (
        "Exact solution φ(x,τ) = ½|x|²/(1+τ) + ½σ²d·ln(1+τ)"
    )
    return aspects


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    results = run_benchmark()
    save_results(results, f'{YOUR_PROBLEM_NAME}_benchmark_results.json')
