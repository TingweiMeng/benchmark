# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A scientific computing benchmark platform for applied math solvers (Hamilton-Jacobi-Bellman PDEs, optimal control, optimal transport, etc.). Python defines benchmarks; a static HTML/JS website displays them.

## Common Commands

**Regenerate website benchmark data after modifying any `*_benchmark.py` file:**
```bash
python extract_benchmark_metadata.py
```
This scans `benchmarks/` for `*_benchmark.py` files and writes `docs/benchmark_data.json`.

**Run a specific benchmark (requires a `solver.py` with `solve_HJB` in the same directory):**
```bash
python benchmarks/HJB/HJB_wholedomain/burgers_benchmark.py
```

**Serve the website locally:**
```bash
python -m http.server 8000
# Then open http://localhost:8000/docs/
```

## Architecture

### Python Backend (`benchmarks/`)
- `benchmarks/utils.py` — Shared utilities: domain setup, error metrics (L1/L2/L∞), plotting, and result I/O. All benchmarks import from here.
- `benchmarks/HJB/HJB_benchmark_template.py` — Template for new HJB benchmarks. Copy this when adding a new problem class. Contains required function signatures: `hamiltonian()`, `initial_condition()`, `reference_solution()`, `get_test_cases()`, `get_benchmark_metadata()`, `run_benchmark()`.
- Each concrete benchmark (e.g., `burgers_benchmark.py`) implements the template for a specific PDE problem.

### Metadata Extraction (`extract_benchmark_metadata.py`)
- Dynamically imports each `*_benchmark.py` using `importlib.util`, mocking missing solver dependencies so metadata can be extracted without a real solver.
- Calls `get_benchmark_metadata()` from each benchmark and writes the aggregated result to `docs/benchmark_data.json`.

### Static Website (`docs/`)
- Pure HTML/CSS/vanilla JS — no build step needed.
- `docs/scripts/benchmarks.js` fetches `benchmark_data.json` at runtime and renders benchmark cards with filterable test case tables.
- `docs/header.html` and `docs/footer.html` are loaded dynamically by `docs/scripts/main.js` into every page.

### Data Flow
```
*_benchmark.py  →  extract_benchmark_metadata.py  →  docs/benchmark_data.json  →  benchmarks.js (frontend)
```

## Adding a New Benchmark

1. Copy `benchmarks/HJB/HJB_benchmark_template.py` to a new directory under the appropriate category (e.g., `benchmarks/HJB/MyProblem/myproblem_benchmark.py`).
2. Implement: `hamiltonian`, `initial_condition`, `reference_solution`, `get_test_cases`, `get_default_params`, `get_benchmark_metadata`.
3. Run `python extract_benchmark_metadata.py` to regenerate `docs/benchmark_data.json`.

## Key Conventions

- Benchmark files must be named `*_benchmark.py` to be discovered by `extract_benchmark_metadata.py`.
- `get_benchmark_metadata()` must return a dict with keys: `name`, `category`, `description`, `hamiltonian_latex`, `tags`, `test_cases`. See existing benchmark for reference.
- User-submitted solvers implement `solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **params)` and are expected to live alongside the benchmark file as `solver.py`.
- Results are saved as `{problem_name}_benchmark_results.json` in the benchmark directory.
