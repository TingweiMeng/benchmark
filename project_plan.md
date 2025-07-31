# Project Plan: Applied Math Benchmark Platform

## 1. Project Overview
The platform will serve as a centralized hub for:
- Maintaining a list of important problems (benchmarks) in applied mathematics.
- Comparing algorithms and their performance on these benchmarks.
- Providing tools for users to contribute benchmarks and algorithms.
- Visualizing results and fostering collaboration in the applied math community.

---

## 2. Features

### 2.1. Benchmarks
- **List of Benchmarks**:
  - Display benchmarks categorized by topics (e.g., HJ PDE, Optimal Control, OT, MFC, JKO/Wasserstein GF).
  - Each benchmark will have:
    - A description of the problem.
    - A button to download the benchmark code (e.g., test functions, datasets).
    - A visualization of the benchmark (e.g., problem setup, solution space).
    - A link to the interface documentation for implementing solvers.
  - Example topics:
    - **HJ PDE**: Hamilton-Jacobi equations.
    - **Optimal Control**: Control problems with constraints.
    - **OT**: Optimal transport problems.
    - **MFC**: Mean-field control problems.
    - **JKO/Wasserstein GF**: Gradient flows in the Wasserstein space.

- **Benchmark Submission**:
  - Provide a button for users to upload their benchmark code.
  - Include a form to submit:
    - Benchmark name.
    - Description.
    - Code (or GitHub link).
    - Reference paper (optional).

---

### 2.2. Algorithms
- **List of Algorithms**:
  - Display a list of algorithms submitted by users or curated by the platform.
  - Each algorithm will have:
    - Name of the algorithm.
    - Author(s).
    - Description (e.g., method, hyperparameters).
    - Link to the implementation (e.g., GitHub repo).
    - Performance metrics (e.g., accuracy, runtime, memory usage).

- **Algorithm Comparison**:
  - Visualize algorithm performance on benchmarks using interactive plots:
    - Example: Dimension vs. Accuracy, Runtime vs. Accuracy.
  - Allow users to filter and sort algorithms by:
    - Benchmark.
    - Performance metrics.
    - Author.

- **Algorithm Submission**:
  - Provide a button for users to upload their algorithm results.
  - Submission options:
    - Upload results directly (e.g., CSV file with metrics).
    - Submit a GitHub link to their implementation.
  - Automate validation of submissions using GitHub Actions:
    - Clone the repository.
    - Run the algorithm on predefined benchmarks.
    - Log results and update the leaderboard.

---

### 2.3. Visualization
- **Benchmark Visualization**:
  - Use interactive plots (e.g., Plotly, Chart.js) to visualize:
    - Problem setup.
    - Solution space.
    - Performance metrics.

- **Algorithm Comparison Visualization**:
  - Provide scatter plots, bar charts, and line plots for:
    - Accuracy vs. Dimension.
    - Runtime vs. Accuracy.
    - Memory usage vs. Accuracy.

---

### 2.4. Wiki and Zotero Integration
- **Wiki Page**:
  - Create a wiki page similar to [MAPF.info](https://mapf.info) to document:
    - Benchmarks.
    - Algorithms.
    - Tutorials and guides.
  - Host the wiki on GitHub Pages or a dedicated platform.

- **Zotero Addon**:
  - Integrate Zotero for managing references to papers and resources.
  - Provide a Zotero library link for users to access curated references.

---

### 2.5. Community Features
- **Discussion Forum**:
  - Use GitHub Discussions or a dedicated forum for users to:
    - Discuss benchmarks and algorithms.
    - Share insights and ask questions.

- **Documentation**:
  - Provide detailed documentation for:
    - Benchmark interfaces.
    - Algorithm submission guidelines.
    - Platform usage.

---

## 3. Technical Design

### 3.1. Frontend
- **Framework**: React or Vue.js for a dynamic and interactive user interface.
- **Pages**:
  - Home Page: Overview of the platform and featured benchmarks/algorithms.
  - Benchmarks Page: List of benchmarks categorized by topics.
  - Algorithms Page: List of algorithms and their performance.
  - Submission Page: Forms for submitting benchmarks and algorithms.
  - Leaderboard Page: Interactive leaderboard for algorithm comparison.
  - Wiki Page: Documentation and resources.

### 3.2. Backend
- **Framework**: Flask or FastAPI for handling submissions and serving data.
- **Endpoints**:
  - `/benchmarks`: Fetch benchmark data.
  - `/algorithms`: Fetch algorithm data.
  - `/submit/benchmark`: Handle benchmark submissions.
  - `/submit/algorithm`: Handle algorithm submissions.

### 3.3. Database
- **Type**: SQLite or PostgreSQL for storing:
  - Benchmarks (name, description, code link, etc.).
  - Algorithms (name, author, metrics, etc.).
  - Submissions (user data, links, etc.).

### 3.4. Automation
- **GitHub Actions**:
  - Automate validation of algorithm submissions:
    - Clone the repository.
    - Run the algorithm on predefined benchmarks.
    - Log results to a database or CSV file.
  - Automate leaderboard updates:
    - Regenerate static HTML pages for the leaderboard.

### 3.5. Hosting
- **Frontend**: GitHub Pages for hosting static files (e.g., HTML, CSS, JS).
- **Backend**: Optional (if needed for dynamic features) – Host on AWS, Heroku, or similar.
- **Database**: Host on a cloud database service (e.g., AWS RDS, Heroku Postgres).

---

## 4. Workflow

1. **Benchmark Creation**:
   - Define benchmark problems and interfaces.
   - Provide downloadable code for benchmarks.
   - Add benchmarks to the platform.

2. **Algorithm Submission**:
   - Users submit algorithms via a form or GitHub link.
   - Validate submissions using GitHub Actions.
   - Update the leaderboard with new results.

3. **Visualization**:
   - Generate interactive plots for benchmarks and algorithms.
   - Update visualizations dynamically based on new submissions.

4. **Wiki and Zotero Integration**:
   - Create a wiki page for documentation and resources.
   - Integrate Zotero for managing references.

5. **Community Engagement**:
   - Encourage discussions and collaboration via forums.
   - Regularly update benchmarks and algorithms.

---

## 5. Future Enhancements
- Add more benchmarks and algorithms.
- Integrate with platforms like Kaggle for competitions.
- Provide APIs for programmatic access to benchmark data.
- Add user authentication for personalized features (e.g., saved submissions, notifications).

---

## 6. References
- [DeepModeling](https://deepmodeling.org)
- [波尔科研空间站](https://dev-tracker.pathfinding.ai)
- [MAPF.info](https://mapf.info)
- [Zotero](https://www.zotero.org)

---

## 7. Next Steps
1. Set up the project structure (frontend, backend, database).
2. Implement the benchmark and algorithm submission workflows.
3. Create a basic frontend for listing benchmarks and algorithms.
4. Add GitHub Actions for automation.
5. Deploy the platform and gather feedback.
