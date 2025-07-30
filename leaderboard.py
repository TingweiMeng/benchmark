import csv
import os

RESULTS_FILE = "results/results.csv"

def log_result(solver_name, error):
    """
    Logs the solver's name and its error to the results file.
    """
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    file_exists = os.path.isfile(RESULTS_FILE)

    with open(RESULTS_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if the file is new
            writer.writerow(["Solver", "Error"])
        writer.writerow([solver_name, error])
