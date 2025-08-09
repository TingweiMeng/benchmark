"""
Benchmark Utilities
==================
Shared utilities for HJB benchmark creation.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from typing import Union, Tuple, List, Dict, Any

# ==========================================
# DOMAIN SETUP UTILITIES
# ==========================================

def setup_spatial_domain(dimension: int, domain_type: str, **params) -> np.ndarray:
    """
    Setup spatial domain based on dimension and parameters.
    
    Args:
        dimension: Spatial dimension
        domain_type: 'grid' or 'points'
        **params: Domain parameters (default: [0,1]^d)
    
    Returns:
        Spatial points for evaluation
    """
    assert domain_type in ['grid', 'points'], "domain_type must be 'grid' or 'points'"
    if domain_type == 'grid':
      if dimension == 1:
        return setup_1d_domain_grid(**params)
      elif dimension == 2:
        return setup_2d_domain_grid(**params)
      else:
        raise NotImplementedError("Grid setup only implemented for 1D and 2D")
    else:  # 'points'
      # randomly sample points in N-D
      return setup_sample_pts(dimension, **params)

def setup_1d_domain_grid(**params) -> np.ndarray:
    """Setup 1D grid points."""
    nx = params.get('nx', 100)
    x_range = params.get('x_range', (0, 1))
    return np.linspace(x_range[0], x_range[1], nx)

def setup_2d_domain_grid(**params) -> np.ndarray:
    """Setup 2D grid points."""
    nx = params.get('nx', 50)
    ny = params.get('ny', 50)
    x_range = params.get('x_range', (0, 1))
    y_range = params.get('y_range', (0, 1))
    
    x = np.linspace(x_range[0], x_range[1], nx)
    y = np.linspace(y_range[0], y_range[1], ny)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    return np.stack([X, Y], axis=-1)

def setup_sample_pts(dimension: int, **params) -> np.ndarray:
    """Setup N-dimensional domain with random points."""
    n_points = params.get('n_points', 1000)
    domain_bounds = params.get('domain_bounds', [(0, 1)] * dimension)
    seed = params.get('seed', 42)
    
    np.random.seed(seed)
    points = np.random.uniform(
        low=[b[0] for b in domain_bounds],
        high=[b[1] for b in domain_bounds],
        size=(n_points, dimension)
    )
    return points

def setup_time_domain(**params) -> np.ndarray:
    """Setup time domain."""
    time_final = params.get('time_final', 0.5)
    nt = params.get('nt', 50)
    return np.linspace(0, time_final, nt)

def get_points_info(spatial_points: np.ndarray) -> str:
    """Get human-readable info about spatial points."""
    if spatial_points.ndim == 1:
        return f"{len(spatial_points)} points"
    elif spatial_points.ndim == 2:
        return f"{spatial_points.shape[0]} points"
    elif spatial_points.ndim == 3:
        return f"{spatial_points.shape[:-1]} grid"
    else:
        return f"shape {spatial_points.shape}"

# ==========================================
# ERROR ANALYSIS
# ==========================================

def compute_error_metrics(u_user: np.ndarray, u_ref: np.ndarray) -> Dict[str, float]:
    """Comprehensive error analysis."""
    abs_error = np.abs(u_user - u_ref)
    
    # Basic metrics
    l1_error = np.mean(abs_error)
    l2_error = np.sqrt(np.mean(abs_error**2))
    linf_error = np.max(abs_error)
    
    # Relative metrics
    ref_norm = np.sqrt(np.mean(u_ref**2))
    rel_l2_error = l2_error / ref_norm if ref_norm > 1e-12 else l2_error
    
    # Additional metrics
    mean_abs_ref = np.mean(np.abs(u_ref))
    rel_linf_error = linf_error / mean_abs_ref if mean_abs_ref > 1e-12 else linf_error
    
    return {
        'l1_error': l1_error,
        'l2_error': l2_error,
        'linf_error': linf_error,
        'relative_l2': rel_l2_error,
        'relative_linf': rel_linf_error
    }

def validate_solution_shape(u_user: np.ndarray, u_ref: np.ndarray, 
                          spatial_points: np.ndarray, time_points: np.ndarray):
    """Validate that solution shapes are consistent."""
    if u_user.shape != u_ref.shape:
        raise ValueError(f"Shape mismatch: user {u_user.shape} vs reference {u_ref.shape}")
    
    # Check if solution shape is compatible with domain
    n_spatial = len(spatial_points) if spatial_points.ndim <= 2 else spatial_points.shape[0]
    n_time = len(time_points)
    
    expected_shapes = [
        (n_spatial, n_time),           # (nx, nt)
        (n_time, n_spatial),           # (nt, nx) - alternative ordering
    ]
    
    # For 2D grids
    if spatial_points.ndim == 3:
        nx, ny = spatial_points.shape[:2]
        expected_shapes.extend([
            (nx, ny, n_time),          # (nx, ny, nt)
            (n_time, nx, ny),          # (nt, nx, ny)
        ])
    
    if u_user.shape not in expected_shapes:
        print(f"Warning: Unexpected solution shape {u_user.shape}")
        print(f"Expected one of: {expected_shapes}")

# ==========================================
# RESULT REPORTING
# ==========================================

def print_results(errors: Dict[str, float], user_time: float):
    """Print formatted results."""
    print(f"L1 Error: {errors['l1_error']:.2e}")
    print(f"L2 Error: {errors['l2_error']:.2e}")
    print(f"L∞ Error: {errors['linf_error']:.2e}")
    print(f"Relative L2: {errors['relative_l2']:.2e}")
    print(f"Solve time: {user_time:.4f}s")
    
    # Performance assessment
    if errors['l2_error'] < 1e-3:
        print("✓ Excellent accuracy!")
    elif errors['l2_error'] < 1e-2:
        print("✓ Good accuracy")
    elif errors['l2_error'] < 1e-1:
        print("○ Acceptable accuracy")
    else:
        print("⚠ Consider improving accuracy")

def print_benchmark_summary(results: List[Dict]):
    """Print comprehensive benchmark summary."""
    print(f"\n{'='*60}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*60}")
    print(f"{'Case':<10} {'Status':<10} {'L2 Error':<12} {'L∞ Error':<12} {'Time (s)':<10}")
    print("-" * 60)
    
    for result in results:
        case_name = f"{result['dimension']}D"
        status = "✓ PASS" if result['success'] else "❌ FAIL"
        
        if result['success']:
            l2_error = f"{result['l2_error']:.2e}"
            linf_error = f"{result['linf_error']:.2e}"
            time_str = f"{result['user_time']:.4f}"
        else:
            l2_error = linf_error = time_str = "N/A"
        
        print(f"{case_name:<10} {status:<10} {l2_error:<12} {linf_error:<12} {time_str:<10}")
    
    # Overall statistics
    successful = [r for r in results if r['success']]
    if successful:
        print(f"\nOverall Performance:")
        print(f"Success rate: {len(successful)}/{len(results)}")
        print(f"Average L2 error: {np.mean([r['l2_error'] for r in successful]):.2e}")
        print(f"Average time: {np.mean([r['user_time'] for r in successful]):.4f}s")

# ==========================================
# VISUALIZATION UTILITIES
# ==========================================

def plot_1d_results(result: Dict, filename: str = None):
    """Create 1D-specific visualization."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    x = result['spatial_points']
    t = result['time_points']
    u_user = result['solution_user']
    u_ref = result['solution_ref']
    
    # Ensure correct orientation
    if u_user.shape[0] == len(t):
        u_user = u_user.T
        u_ref = u_ref.T
    
    # Space-time plots
    im1 = axes[0,0].contourf(x, t, u_user.T, levels=20, cmap='viridis')
    axes[0,0].set_title('User Solution')
    axes[0,0].set_xlabel('x')
    axes[0,0].set_ylabel('t')
    plt.colorbar(im1, ax=axes[0,0])
    
    im2 = axes[0,1].contourf(x, t, u_ref.T, levels=20, cmap='viridis')
    axes[0,1].set_title('Reference Solution')
    axes[0,1].set_xlabel('x')
    axes[0,1].set_ylabel('t')
    plt.colorbar(im2, ax=axes[0,1])
    
    # Error plot
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
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"1D visualization saved as '{filename}'")
    plt.show()

def plot_2d_results(result: Dict, filename: str = None):
    """Create 2D-specific visualization."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    u_user = result['solution_user']
    u_ref = result['solution_ref']
    
    # Get final time solutions
    if u_user.ndim == 3:
        u_user_final = u_user[:, :, -1]
        u_ref_final = u_ref[:, :, -1]
    else:
        # Reshape if needed
        spatial_shape = result['spatial_points'].shape[:2]
        u_user_final = u_user[:, -1].reshape(spatial_shape)
        u_ref_final = u_ref[:, -1].reshape(spatial_shape)
    
    # Solutions and error
    im1 = axes[0,0].contourf(u_user_final, levels=20, cmap='viridis')
    axes[0,0].set_title('User Solution (final)')
    plt.colorbar(im1, ax=axes[0,0])
    
    im2 = axes[0,1].contourf(u_ref_final, levels=20, cmap='viridis')
    axes[0,1].set_title('Reference Solution (final)')
    plt.colorbar(im2, ax=axes[0,1])
    
    error_final = np.abs(u_user_final - u_ref_final)
    im3 = axes[0,2].contourf(error_final, levels=20, cmap='hot')
    axes[0,2].set_title('Absolute Error (final)')
    plt.colorbar(im3, ax=axes[0,2])
    
    # Cross-sections
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
    
    # Error evolution over time
    if u_user.ndim == 3:
        t = result['time_points']
        l2_errors = [np.sqrt(np.mean((u_user[:,:,i] - u_ref[:,:,i])**2)) 
                     for i in range(len(t))]
        axes[1,2].semilogy(t, l2_errors)
        axes[1,2].set_title('L2 Error Evolution')
        axes[1,2].set_xlabel('Time')
        axes[1,2].grid(True)
    
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"2D visualization saved as '{filename}'")
    plt.show()

def plot_scaling_analysis(results: List[Dict], filename: str = None):
    """Create scaling analysis across dimensions."""
    successful = [r for r in results if r['success']]
    
    if len(successful) < 2:
        print("Need at least 2 successful results for scaling analysis")
        return
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    dims = [r['dimension'] for r in successful]
    l2_errors = [r['l2_error'] for r in successful]
    linf_errors = [r['linf_error'] for r in successful]
    times = [r['user_time'] for r in successful]
    rel_errors = [r['relative_l2'] for r in successful]
    
    # Error scaling
    ax1.semilogy(dims, l2_errors, 'bo-', linewidth=2, markersize=8, label='L2')
    ax1.semilogy(dims, linf_errors, 'ro-', linewidth=2, markersize=8, label='L∞')
    ax1.set_xlabel('Dimension')
    ax1.set_ylabel('Absolute Error')
    ax1.set_title('Error vs Dimension')
    ax1.legend()
    ax1.grid(True)
    
    # Relative error
    ax2.semilogy(dims, rel_errors, 'go-', linewidth=2, markersize=8)
    ax2.set_xlabel('Dimension')
    ax2.set_ylabel('Relative L2 Error')
    ax2.set_title('Relative Error vs Dimension')
    ax2.grid(True)
    
    # Time scaling
    ax3.semilogy(dims, times, 'mo-', linewidth=2, markersize=8)
    ax3.set_xlabel('Dimension')
    ax3.set_ylabel('Solve Time (seconds)')
    ax3.set_title('Performance vs Dimension')
    ax3.grid(True)
    
    # Error vs time tradeoff
    ax4.loglog(times, l2_errors, 'ko', markersize=8)
    for i, dim in enumerate(dims):
        ax4.annotate(f'{dim}D', (times[i], l2_errors[i]), 
                    xytext=(5, 5), textcoords='offset points')
    ax4.set_xlabel('Solve Time (seconds)')
    ax4.set_ylabel('L2 Error')
    ax4.set_title('Error vs Time Tradeoff')
    ax4.grid(True)
    
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Scaling analysis saved as '{filename}'")
    plt.show()

# ==========================================
# RESULT MANAGEMENT
# ==========================================

def save_results(results: List[Dict], filename: str):
    """Save benchmark results to JSON file."""
    # Clean results for JSON serialization
    results_clean = []
    for r in results:
        r_clean = {k: v for k, v in r.items() 
                  if k not in ['solution_user', 'solution_ref', 'spatial_points', 'time_points']}
        # Convert numpy types to Python types
        for key, value in r_clean.items():
            if isinstance(value, np.floating):
                r_clean[key] = float(value)
            elif isinstance(value, np.integer):
                r_clean[key] = int(value)
        results_clean.append(r_clean)
    
    with open(filename, 'w') as f:
        json.dump(results_clean, f, indent=2)
    print(f"Results saved to '{filename}'")

def load_results(filename: str) -> List[Dict]:
    """Load benchmark results from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)