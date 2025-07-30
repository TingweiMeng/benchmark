import csv

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Benchmark Leaderboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f4f4f4; }}
    </style>
</head>
<body>
    <h1>Benchmark Leaderboard</h1>
    <table>
        <thead>
            <tr>
                <th>Solver</th>
                <th>Error</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</body>
</html>
"""

def generate_leaderboard(results_file, output_file):
    rows = ""
    try:
        with open(results_file, "r") as f:
            reader = csv.DictReader(f)
            sorted_results = sorted(reader, key=lambda x: float(x["Error"]))
            for row in sorted_results:
                rows += f"<tr><td>{row['Solver']}</td><td>{row['Error']}</td></tr>\n"
    except FileNotFoundError:
        rows = "<tr><td colspan='2'>No results available</td></tr>"

    with open(output_file, "w") as f:
        f.write(HTML_TEMPLATE.format(rows=rows))

if __name__ == "__main__":
    generate_leaderboard("results/results.csv", "docs/leaderboard.html")