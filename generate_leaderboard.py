import csv
import os

MAIN_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benchmark Dashboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Benchmark Dashboard</h1>
    <p>Welcome to the benchmark dashboard. Select a benchmark to view its leaderboard and visualizations:</p>
    <ul>
        {benchmark_links}
    </ul>
</body>
</html>
"""

BENCHMARK_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{benchmark_name} Leaderboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>{benchmark_name} Leaderboard</h1>
    <nav>
        <a href="index.html">Back to Dashboard</a>
    </nav>
    <table>
        <thead>
            <tr>
                <th>Solver</th>
                <th>Error</th>
                <th>Author</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    <div id="visualization" style="width: 100%; height: 400px;"></div>
    <script src="visualizations/{benchmark_plot_js}"></script>
</body>
</html>
"""

def generate_dashboard(benchmarks, output_file):
    """
    Generate the main dashboard listing all benchmarks.
    """
    benchmark_links = "\n".join(
        [f'<li><a href="{benchmark["html_file"]}">{benchmark["name"]}</a></li>' for benchmark in benchmarks]
    )
    with open(output_file, "w") as f:
        f.write(MAIN_DASHBOARD_TEMPLATE.format(benchmark_links=benchmark_links))

def generate_leaderboard(results_file, output_file, benchmark_name, benchmark_plot_js):
    """
    Generate an individual benchmark leaderboard page.
    """
    rows = ""
    try:
        with open(results_file, "r") as f:
            reader = csv.DictReader(f)
            sorted_results = sorted(reader, key=lambda x: float(x["Error"]))
            for row in sorted_results:
                rows += f"<tr><td>{row['Solver']}</td><td>{row['Error']}</td><td>{row['Author']}</td><td>{row['Description']}</td></tr>\n"
    except FileNotFoundError:
        rows = "<tr><td colspan='4'>No results available</td></tr>"

    with open(output_file, "w") as f:
        f.write(BENCHMARK_TEMPLATE.format(
            benchmark_name=benchmark_name,
            rows=rows,
            benchmark_plot_js=benchmark_plot_js
        ))

if __name__ == "__main__":
    # Define benchmarks
    benchmarks = [
        {
            "name": "HJ 1D Benchmark",
            "results_file": "results/hj_1d.csv",
            "html_file": "docs/hj_1d.html",
            "plot_js": "hj_1d_plot.js"
        },
        {
            "name": "Other Benchmark",
            "results_file": "results/other_benchmark.csv",
            "html_file": "docs/other_benchmark.html",
            "plot_js": "other_benchmark_plot.js"
        }
    ]

    # Generate individual benchmark pages
    for benchmark in benchmarks:
        generate_leaderboard(
            benchmark["results_file"],
            benchmark["html_file"],
            benchmark["name"],
            benchmark["plot_js"]
        )

    # Generate main dashboard
    generate_dashboard(benchmarks, "docs/index.html")