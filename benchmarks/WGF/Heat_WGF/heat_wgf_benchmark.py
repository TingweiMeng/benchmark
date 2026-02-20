"""
Wasserstein Gradient Flow — Heat Equation Benchmark
====================================================
Benchmark for the Wasserstein gradient flow of the Boltzmann entropy,
which corresponds to the heat / Fokker-Planck equation.

PDE (density formulation):
    ∂ρ/∂t = ½σ²Δρ

Hopf-Cole transform φ = -σ² log ρ converts this to a viscous HJB:
    ∂φ/∂t + ½|∇φ|² - ½σ²Δφ = 0

Test Cases — bimodal Gaussian initial density:
    ρ₀(x) = ½ N(x; -μ, σ₀²I) + ½ N(x; +μ, σ₀²I)

Analytical solution at time t:
    ρₜ(x) = ½ N(x; -μ, (σ₀²+σ²t)I) + ½ N(x; +μ, (σ₀²+σ²t)I)

Reference potential:
    φ(x, t) = -σ² log ρₜ(x)  (up to an additive constant)

The bimodal structure tests solvers' ability to resolve non-convex potentials
and multi-modal distributions — a key challenge absent from unimodal benchmarks.

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
YOUR_PROBLEM_NAME = "Heat_WGF"


def hamiltonian(p, **params):
    """
    Hamiltonian: H(p) = ½|p|².
    The diffusion coefficient σ is passed via params to the solver.

    Args:
        p: Gradient of potential, shape [n_pts, dim]
    Returns:
        H(p), shape [n_pts]
    """
    assert isinstance(p, np.ndarray) and p.ndim == 2
    return 0.5 * np.sum(p**2, axis=-1)


def initial_condition(spatial_points, **params):
    """
    Initial Hopf-Cole potential from bimodal Gaussian density.
    φ(x, 0) = -σ² log ρ₀(x)  (shifted to be zero-mean for numerical stability)

    Args:
        spatial_points: shape [n_pts, dim]
    Returns:
        φ(x, 0), shape [n_pts]
    """
    assert isinstance(spatial_points, np.ndarray) and spatial_points.ndim == 2
    sigma = params.get('sigma', 0.3)
    sigma0 = params.get('sigma0', 1.0)
    dim = spatial_points.shape[-1]
    mu_val = params.get('mu_val', 1.5)
    mu = np.zeros(dim)
    mu[0] = mu_val  # shift along first coordinate only

    log_rho = _log_bimodal(spatial_points, mu, sigma0, dim)
    phi = -sigma**2 * log_rho
    phi -= phi.mean()  # zero-mean normalization (additive constant gauge)
    return phi


def reference_solution(spatial_points, time_points, **params):
    """
    Analytical Hopf-Cole potential from evolved bimodal Gaussian density.
    φ(x, t) = -σ² log ρₜ(x)
    """
    sigma = params.get('sigma', 0.3)
    sigma0 = params.get('sigma0', 1.0)

    if spatial_points.ndim == 1:
        return _reference_1d(spatial_points, time_points, sigma, sigma0, params)
    elif spatial_points.ndim == 3:
        return _reference_2d_grid(spatial_points, time_points, sigma, sigma0, params)
    else:
        return _reference_points(spatial_points, time_points, sigma, sigma0, params)


def _log_bimodal(x, mu, sigma_t, dim):
    """Compute log of bimodal Gaussian density (unnormalized log, for numerical stability)."""
    def log_gaussian(pts, center, s):
        diff = pts - center
        return -0.5 * np.sum(diff**2, axis=-1) / s**2

    if x.ndim == 1:
        x2d = x.reshape(-1, 1)
    else:
        x2d = x.reshape(-1, dim) if x.ndim > 2 else x

    log_p1 = log_gaussian(x2d, +mu, sigma_t)
    log_p2 = log_gaussian(x2d, -mu, sigma_t)
    # log(0.5 * exp(a) + 0.5 * exp(b)) = log-sum-exp
    log_max = np.maximum(log_p1, log_p2)
    log_rho = log_max + np.log(np.exp(log_p1 - log_max) + np.exp(log_p2 - log_max)) - np.log(2)
    return log_rho.reshape(x.shape[:-1]) if x.ndim > 2 else log_rho


def _reference_1d(x, t, sigma, sigma0, params):
    dim = 1
    mu_val = params.get('mu_val', 1.5)
    mu = np.array([mu_val])
    x2d = x.reshape(-1, 1)
    u = np.zeros((len(x), len(t)))
    for k, tk in enumerate(t):
        sigma_t = np.sqrt(sigma0**2 + sigma**2 * tk)
        log_rho = _log_bimodal(x2d, mu, sigma_t, dim)
        phi = -sigma**2 * log_rho
        phi -= phi.mean()
        u[:, k] = phi
    return u


def _reference_2d_grid(spatial_points, t, sigma, sigma0, params):
    dim = 2
    nx, ny, _ = spatial_points.shape
    mu_val = params.get('mu_val', 1.5)
    mu = np.zeros(dim)
    mu[0] = mu_val
    pts = spatial_points.reshape(-1, dim)
    u = np.zeros((nx, ny, len(t)))
    for k, tk in enumerate(t):
        sigma_t = np.sqrt(sigma0**2 + sigma**2 * tk)
        log_rho = _log_bimodal(pts, mu, sigma_t, dim)
        phi = -sigma**2 * log_rho
        phi -= phi.mean()
        u[:, :, k] = phi.reshape(nx, ny)
    return u


def _reference_points(spatial_points, t, sigma, sigma0, params):
    n_pts, dim = spatial_points.shape
    mu_val = params.get('mu_val', 1.5)
    mu = np.zeros(dim)
    mu[0] = mu_val
    u = np.zeros((n_pts, len(t)))
    for k, tk in enumerate(t):
        sigma_t = np.sqrt(sigma0**2 + sigma**2 * tk)
        log_rho = _log_bimodal(spatial_points, mu, sigma_t, dim)
        phi = -sigma**2 * log_rho
        phi -= phi.mean()
        u[:, k] = phi
    return u


# ==========================================
# TEST CONFIGURATION
# ==========================================

def get_test_cases():
    return [
        (1,  {'nx': 100,            'domain_type': 'grid',   'sigma': 0.3, 'sigma0': 1.0}),
        (2,  {'nx': 50, 'ny': 50,  'domain_type': 'grid',   'sigma': 0.3, 'sigma0': 1.0}),
        (3,  {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.3, 'sigma0': 1.0}),
        (5,  {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.3, 'sigma0': 1.0}),
        (10, {'n_points': 1000,     'domain_type': 'points', 'sigma': 0.3, 'sigma0': 1.0}),
    ]


def get_default_params():
    return {
        'time_final': 1.0,
        'nt': 50,
        'x_range': (-4, 4),
        'y_range': (-4, 4),
        'sigma': 0.3,
        'sigma0': 1.0,
        'mu_val': 1.5,
    }


# ==========================================
# BENCHMARK RUNNER
# ==========================================

def run_test_case(dimension, test_params):
    print(f"\nTest Case: {dimension}D")
    print("-" * 20)

    params = {**get_default_params(), **test_params}
    params['domain_bounds'] = [(-4, 4)] * dimension

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
    """Visualize WGF benchmark results."""
    successful = [r for r in results if r['success']]
    if not successful:
        return

    for i, result in enumerate(successful):
        dim = result['dimension']
        if dim == 1:
            plot_1d_results(result, filename=f'wgf_heat_1d_case{i+1}.png')
        elif dim == 2:
            plot_2d_results(result, filename=f'wgf_heat_2d_case{i+1}.png')

    plot_scaling_analysis(successful, filename='wgf_heat_scaling_analysis.png')


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
        "name": "Wasserstein Gradient Flow (Heat Equation)",
        "category": "WGF",
        "short_description": (
            "Wasserstein gradient flow of the Boltzmann entropy (heat equation) "
            "with bimodal Gaussian initial density"
        ),
        "equation": "∂φ/∂t + ½|∇φ|² - ½σ²Δφ = 0  (Hopf-Cole form of ∂ρ/∂t = ½σ²Δρ)",
        "initial_condition": "φ(x,0) = -σ² log[½N(x;+μ,σ₀²I) + ½N(x;-μ,σ₀²I)]",
        "background": (
            "Gradient flow of Boltzmann entropy F[ρ]=∫ρ log ρ dx in Wasserstein space. "
            "Bimodal IC tests multi-modal structure propagation."
        ),
        "applications": ["Sampling algorithms", "Score-based generative models", "Diffusion models"],
    }


def get_physics_regime(params):
    sigma = params.get('sigma', 0.3)
    return f"Diffusive (σ={sigma})"


def get_case_description(dimension, params, problem_info):
    sigma = params.get('sigma', 0.3)
    pt = "grid" if 'nx' in params else "random points"
    return f"{dimension}D WGF heat, σ={sigma} ({pt})"


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
    aspects["multi_modal"] = (
        "Bimodal initial density tests handling of non-convex potentials"
    )
    aspects["analytical_reference"] = (
        "Analytical reference via evolving bimodal Gaussian under heat flow"
    )
    return aspects


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    results = run_benchmark()
    save_results(results, f'{YOUR_PROBLEM_NAME}_benchmark_results.json')
