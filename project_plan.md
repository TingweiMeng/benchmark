# Project Plan: Applied Math Benchmark Platform

## 1. Project Overview
The platform will serve as a centralized hub for:
- Maintaining a list of important problems (benchmarks) in applied mathematics.
- Comparing algorithms and their performance on these benchmarks.
- Providing tools for users to contribute benchmarks and algorithms.
- Visualizing results and fostering collaboration in the applied math community.

### 1.1. Directory Structure
benchmark/
├── benchmarks/                           # Benchmark definitions and test scripts
│   ├── <topic>/                          # Topic-level folder (e.g., HJB PDE, Optimal Control)
│   │   ├── <class_of_problems>/          # Class of problems (e.g., periodic BC, unbounded domain)
│   │   │   ├── benchmark_code.py         # Combined benchmark implementation and test script
│   │   │   ├── details.md                # Problem description and references
├── docs/                                 # Static HTML files for the platform
│   ├── index.html                        # Main dashboard
│   ├── benchmarks.html                   # Benchmarks page
│   ├── submission.html                   # Submission page
│   ├── algorithms.html                   # Algorithms page
│   ├── leaderboard.html                  # Leaderboard page (if applicable in the future)
│   ├── header.html                       # Shared header component
│   ├── footer.html                       # Shared footer component
│   ├── user_guide.html                   # User guide page
│   ├── scripts/                          # JavaScript files for interactivity
│   │   ├── main.js                       # Shared JavaScript logic
│   │   ├── benchmarks.js                 # JavaScript for benchmarks page
│   │   ├── submission.js                 # JavaScript for submission page
│   │   ├── algorithms.js                 # JavaScript for algorithms page
│   ├── styles.css                        # Shared CSS for styling
├── results/                              # User-submitted results (optional, for local testing)
│   ├── <topic>_<class>.csv               # Results for specific benchmarks
├── README.md                             # Project overview and quick start guide
├── project_plan.md                       # Detailed project plan and roadmap
---

## 2. Features

### 2.1. Benchmarks
- **Structure**:
  - Benchmarks are organized hierarchically:
    - **Topic**: High-level categories (e.g., HJB PDE, Optimal Control, OT, etc.).
    - **Classes of Problems**: Subcategories within each topic (e.g., HJB PDE with unbounded domain, periodic BC, Dirichlet BC).
    - **Specific Cases**: Individual problems (e.g., Burgers' equation).
  - Each specific case will include:
    - **benchmark_code.py**: Combined file containing:
      - Problem definition (Hamiltonian, initial conditions)
      - Reference solution implementation
      - Test script for evaluating user solutions
    - **details.md**: Problem description, references, and usage instructions
    - These details will be hidden in a **collapsible penal** for better organization.

- **Single File Design**:
  - All benchmark-related code is contained in one downloadable Python file
  - Users only need to download one file to get started
  - The file includes:
    - Problem definition functions
    - Reference solution for comparison
    - Test function that users can call with their solver
    - Usage examples and documentation

- **User Workflow**:
  - Users download the single benchmark_code.py file
  - Users import their solver into the benchmark code and:
    - Run the script locally and upload the results.
    - Or provide a GitHub repository link with the test script in a specific location.
  - If a GitHub link is provided, we will use **GitHub Actions** to run the test script and validate the results.
  - The results will be stored in a database and displayed on the platform.
  - Other things a user may provide: benchmark name, author, description, and references.

---

### 2.2. Visualization
- **Structure**:
  - The webpage will display benchmarks in a hierarchical structure:
    - **Topic** → **Classes of Problems** → **Specific Cases**.
  - For each specific case, the webpage will show:
    - Problem description.
    - References.
    - A download button for the benchmark code.
    - These details will be hidden in a **collapsible menu** (下拉菜单) for better organization.

- **Interactive Visualizations**:
  - Use interactive plots (e.g., Plotly, Chart.js) to visualize:
    - Problem setup.
    - Solution space.
    - Performance metrics.

---

### 2.3. Algorithms
- **Submission**:
  - Users can submit their algorithms via:
    - A form to upload results (e.g., CSV file with metrics).
    - A GitHub link to their implementation.
  - Submissions will be validated using **GitHub Actions**:
    - Clone the repository.
    - Run the algorithm on predefined benchmarks.
    - Log results and update the leaderboard.

- **Comparison**:
  - Visualize algorithm performance on benchmarks using interactive plots:
    - Example: Dimension vs. Accuracy, Runtime vs. Accuracy.
  - Allow users to filter and sort algorithms by:
    - Benchmark.
    - Performance metrics.
    - Author.

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

### 2.6. User Guidance
- **Primary Location**: `docs/user_guide.html`
  - Comprehensive guide covering benchmark usage, solver implementation, and submission process
  - Step-by-step instructions with examples
  - Links to relevant resources and pages
  - Accessible through the main navigation menu

- **Navigation Integration**: 
  - Added "User Guide" to the main navigation menu in `header.html`
  - Available from any page on the platform for easy access

- **Secondary Locations**: Contextual links from key pages
  - `benchmarks.html`: Link to user guide for benchmark usage
  - `submission.html`: Link to user guide for submission instructions

- **Benchmark-Specific Guidance**: In individual `details.md` files
  - Problem-specific instructions
  - Solver interface requirements
  - Testing and submission guidelines
  
---

## 3. Technical Design

### 3.1. Frontend
- **Framework**: React or Vue.js for a dynamic and interactive user interface.
- **Pages**:
  - Home Page: Overview of the platform and featured benchmarks/algorithms.
  - Benchmarks Page: Hierarchical structure for topics, classes of problems, and specific cases.
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
