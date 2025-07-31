import csv
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benchmark Leaderboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Benchmark Leaderboard</h1>
    <nav>
        <a href="hj_1d.html">HJ 1D</a>
        <a href="other_benchmark.html">Other Benchmark</a>
    </nav>
    <h2>{benchmark_name}</h2>
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
    <script src="visualizations/{benchmark_plot_js}"></script>
</body>
</html>
"""

def generate_leaderboard(results_file, output_file, benchmark_name, benchmark_plot_js):
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
        f.write(HTML_TEMPLATE.format(
            benchmark_name=benchmark_name,
            rows=rows,
            benchmark_plot_js=benchmark_plot_js
        ))

if __name__ == "__main__":
    generate_leaderboard("results/hj_1d.csv", "docs/hj_1d.html", "HJ 1D Benchmark", "hj_1d_plot.js")
    generate_leaderboard("results/other_benchmark.csv", "docs/other_benchmark.html", "Other Benchmark", "other_benchmark_plot.js")