"""
Wasserstein-2 Optimal Transport Benchmark
==========================================
Benchmark for the L2 optimal transport problem via the Benamou-Brenier
fluid-dynamics formulation.

Problem: Minimize ∫₀¹ ∫ ½|v(x,t)|² ρ(x,t) dx dt
Subject to: ∂ρ/∂t + ∇·(ρv) = 0, ρ(·,0)=ρ₀, ρ(·,1)=ρ₁

Dual HJ equation for the Kantorovich potential φ:
    ∂φ/∂t + ½|∇φ|² = 0

Test Cases:
- Gaussian-to-Gaussian transport: ρ₀ = N(0, I), ρ₁ = N(μ, I)
- Analytical reference: φ(x,t) = μ·x - ½|μ|²·t  (μ = μ₁ - μ₀)
- Dimensions: 1D, 2D, 3D, 5D, 10D

Required solver interface:
    solve_HJB(hamiltonian, initial_condition, spatial_points, time_points) -> solution
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
YOUR_PROBLEM_NAME = "W2_Gaussian_Transport"

def hamiltonian(p, **params):
    """
    Hamiltonian for Wasserstein-2 optimal transport.
    H(p) = ½|p|²  (L2 kinetic energy)

    Args:
        p: Momentum variable, np array shape [n_pts, dim]
    Returns:
        H(p), shape [n_pts]
    """
    assert isinstance(p, np.ndarray) and p.ndim == 2
    return 0.5 * np.sum(p**2, axis=-1)


def initial_condition(spatial_points, **params):
    """
    Kantorovich potential at t=0 for Gaussian-to-Gaussian transport.
    φ(x, 0) = (μ₁ - μ₀) · x

    Args:
        spatial_points: shape [n_pts, dim]
    Returns:
        φ(x, 0), shape [n_pts]
    """
    assert isinstance(spatial_points, np.ndarray) and spatial_points.ndim == 2
    dim = spatial_points.shape[-1]
    mu0 = np.array(params.get('mu0', [0.0] * dim))
    mu1 = np.array(params.get('mu1', [1.0 / np.sqrt(dim)] * dim))
    displacement = mu1 - mu0
    return spatial_points @ displacement


def reference_solution(spatial_points, time_points, **params):
    """
    Analytical Kantorovich potential for Gaussian-to-Gaussian transport.
    φ(x, t) = (μ₁ - μ₀) · x  -  ½|μ₁ - μ₀|² · t

    Verification: ∂φ/∂t = -½|d|², ∇φ = d, ½|∇φ|² = ½|d|²  →  HJB satisfied ✓
    """
    if spatial_points.ndim == 1:
        return _reference_1d(spatial_points, time_points, **params)
    elif spatial_points.ndim == 3:
        return _reference_2d_grid(spatial_points, time_points, **params)
    else:
        return _reference_points(spatial_points, time_points, **params)


def _displacement_and_w2(dim, params):
    mu0 = np.array(params.get('mu0', [0.0] * dim))
    mu1 = np.array(params.get('mu1', [1.0 / np.sqrt(dim)] * dim))
    d = mu1 - mu0
    return d, np.sum(d**2)


def _reference_1d(x, t, **params):
    d, w2_sq = _displacement_and_w2(1, params)
    # x shape: (nx,), return shape (nx, nt)
    phi_x = x * d[0]
    u = np.zeros((len(x), len(t)))
    for k, tk in enumerate(t):
        u[:, k] = phi_x - 0.5 * w2_sq * tk
    return u


def _reference_2d_grid(spatial_points, t, **params):
    # spatial_points shape: (nx, ny, 2)
    nx, ny, _ = spatial_points.shape
    d, w2_sq = _displacement_and_w2(2, params)
    phi_x = spatial_points @ d  # (nx, ny)
    u = np.zeros((nx, ny, len(t)))
    for k, tk in enumerate(t):
        u[:, :, k] = phi_x - 0.5 * w2_sq * tk
    return u


def _reference_points(spatial_points, t, **params):
    # spatial_points shape: (n_pts, dim)
    n_pts, dim = spatial_points.shape
    d, w2_sq = _displacement_and_w2(dim, params)
    phi_x = spatial_points @ d  # (n_pts,)
    u = np.zeros((n_pts, len(t)))
    for k, tk in enumerate(t):
        u[:, k] = phi_x - 0.5 * w2_sq * tk
    return u


# ==========================================
# TEST CONFIGURATION
# ==========================================

def get_test_cases():
    return [
        (1,  {'nx': 100,              'domain_type': 'grid'}),
        (2,  {'nx': 50, 'ny': 50,    'domain_type': 'grid'}),
        (3,  {'n_points': 1000,       'domain_type': 'points'}),
        (5,  {'n_points': 1000,       'domain_type': 'points'}),
        (10, {'n_points': 1000,       'domain_type': 'points'}),
    ]


def get_default_params():
    return {
        'time_final': 1.0,
        'nt': 50,
        'x_range': (-2, 2),
        'y_range': (-2, 2),
        'domain_bounds': [(-2, 2)],   # per-dim, extended at runtime
    }


# ==========================================
# BENCHMARK RUNNER
# ==========================================

def run_test_case(dimension, test_params):
    print(f"\nTest Case: {dimension}D")
    print("-" * 20)

    params = {**get_default_params(), **test_params}
    # Extend domain bounds to match dimension
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
    """Visualize OT benchmark results."""
    successful = [r for r in results if r['success']]
    if not successful:
        return

    for i, result in enumerate(successful):
        dim = result['dimension']
        if dim == 1:
            plot_1d_results(result, filename=f'ot_w2_gaussian_1d_case{i+1}.png')
        elif dim == 2:
            plot_2d_results(result, filename=f'ot_w2_gaussian_2d_case{i+1}.png')

    plot_scaling_analysis(successful, filename='ot_w2_gaussian_scaling.png')


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
        "name": "Wasserstein-2 Gaussian Transport",
        "category": "OT",
        "short_description": "L2 optimal transport between Gaussian distributions via the Benamou-Brenier formulation",
        "equation": "∂φ/∂t + ½|∇φ|² = 0",
        "initial_condition": "φ(x,0) = (μ₁-μ₀)·x",
        "background": "Benamou-Brenier fluid-dynamic formulation of Wasserstein-2 optimal transport",
        "applications": ["Generative models", "Domain adaptation", "Image morphing"],
    }


def get_physics_regime(params):
    return "Optimal Transport"


def get_case_description(dimension, params, problem_info):
    pt = "grid" if 'nx' in params else "random points"
    return f"{dimension}D Gaussian transport ({pt})"


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
    aspects["analytical_reference"] = (
        "Exact Kantorovich potential available for Gaussian-to-Gaussian transport"
    )
    return aspects


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    results = run_benchmark()
    save_results(results, f'{YOUR_PROBLEM_NAME}_benchmark_results.json')
