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

(To test the code locally, run "python3 -m http.server --directory . 8000 " and open http://localhost:8000 in your browser.)
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

## 8. Benchmark Design Philosophy and Template Framework

### 8.1 Hierarchical Structure

Our benchmark platform follows a **four-level hierarchy** to organize problems systematically:

```
Level 1: HJB Category (e.g., HJB_wholedomain, HJB_periodic, HJB_dirichlet)
    ↓
Level 2: Problem Type (e.g., burgers, eikonal, allen_cahn)
    ↓  
Level 3: Specific Problem (e.g., burgers_sine_ic, burgers_gaussian_ic, burgers_shock_ic)
    ↓
Level 4: Test Cases (e.g., 1D_grid, 2D_grid, 3D_points, 5D_points, 10D_points)
```

**Example Full Path:** `HJB_wholedomain/burgers/burgers_sine_ic/[1D_grid, 2D_grid, 3D_points, ...]`

### 8.2 Template Design Principles

#### 8.2.1 Solver Interface Standardization
All HJB benchmarks use the **same solver interface**:
```python
solve_HJB(hamiltonian, initial_condition, spatial_points, time_points, **params) -> solution
```

This allows:
- **Consistent user experience** across all benchmarks
- **Algorithm comparison** on the same interface
- **Easy benchmark addition** with minimal learning curve

#### 8.2.2 Multi-Dimensional and Multi-Domain Support
Each benchmark tests algorithms across **multiple scenarios**:

**Spatial Dimensions:**
- 1D, 2D: Grid-based evaluation (traditional PDE solvers)
- 3D+: Point-wise evaluation (high-dimensional methods)

**Domain Types:**
- `grid`: Structured grids for traditional finite difference/element methods
- `points`: Arbitrary point clouds for meshless/ML methods

**Rationale:** Different algorithms excel in different settings. A finite difference solver may be excellent on 2D grids but cannot handle arbitrary point clouds or high dimensions.

#### 8.2.3 Comprehensive Testing Strategy
Each benchmark provides **multiple test cases** to evaluate:

1. **Accuracy**: L1, L2, L∞, and relative errors
2. **Scalability**: Performance across dimensions 1D → 2D → 3D → 5D → 10D
3. **Flexibility**: Grid-based vs point-based evaluation
4. **Robustness**: Different initial conditions and parameters

#### 8.2.4 Reference Solution Strategy
- **Template**: Provides empty `reference_solution()` function
- **Implementation**: Each specific problem implements high-accuracy reference
- **Methods**: Analytical solutions when available, otherwise high-order numerical methods with fine grids
- **No Timing Comparison**: Reference timing excluded from performance metrics (unfair comparison)

### 8.3 Leaderboard Categorization

Algorithms will be **categorized by capabilities** on the leaderboard:

**Algorithm Categories:**
- `Grid_1D`: Works only on 1D grids
- `Grid_2D`: Works on 1D and 2D grids  
- `Grid_ND`: Works on grids up to N dimensions
- `Points_ND`: Works on arbitrary point sets up to N dimensions
- `Universal`: Works on both grids and points, all tested dimensions

**Display Strategy:**
- Show algorithm performance only for **supported categories**
- Clear **capability indicators** (✓ 1D Grid, ✓ 2D Grid, ✗ 3D Points, etc.)
- **Separate rankings** for different capability classes

### 8.4 Implementation Timeline

#### Phase 1.1: Template Refinement (8-4 to 8-6)
- [ ] Finalize template structure with hierarchical design
- [ ] Implement flexible domain setup utilities
- [ ] Create comprehensive error metrics framework
- [ ] Test template with Burgers implementation

#### Phase 1.2: Multi-Case Testing (8-6 to 8-8)
- [ ] Implement all test cases for Burgers benchmark
- [ ] Add visualization suite for different dimensions
- [ ] Create scaling analysis tools
- [ ] Validate reference solution accuracy

#### Phase 1.3: Documentation and Examples (8-8 to 8-10)
- [ ] Write comprehensive template documentation
- [ ] Create step-by-step guide for new benchmark creation
- [ ] Document the hierarchical structure
- [ ] Provide algorithm interface examples

### 8.5 Quality Assurance

**Template Validation:**
- Every new benchmark must pass **template compliance check**
- Standard error metrics and visualization requirements
- Consistent interface and documentation format

**Reference Solution Validation:**
- Cross-validation with analytical solutions when available
- Convergence testing with grid refinement
- Comparison with literature results when possible

**Algorithm Categorization:**
- Automatic detection of algorithm capabilities based on test results
- Clear capability documentation for users
- Performance tracking across different scenarios

This framework ensures **scalability**, **consistency**, and **comprehensive evaluation** while accommodating the diverse landscape of HJB PDE solvers.

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

## 7. Working Progress and Next Steps

### Working Progress
- **7-30-2025**: Initial project setup and basic structure (code and webpage, algorithm submission workflows)
- **8-1-2025**: Implemented the first benchmark (Burgers) for Hamilton-Jacobi-Bellman PDEs: the pipeline of benchmark and user_guide

### Phase 1: Core Benchmark Platform (August 2025)
**Target Completion: August 15, 2025**

#### Week 1: Benchmark Content Expansion (8-3 to 8-8)
- **8-4-2025**: 
  - [ ] Add one more HJB PDE benchmarks (Eikonal equation)
  - [ ] Test code upload functionality
  - [ ] Create benchmark template structure for consistency

- **8-5-2025**: 
  - [ ] Add one optimal control benchmark (differential drive)

- **8-8-2025**: 
  - [ ] Improve benchmarks.html navigation and organization
  - [ ] Add better descriptions and categorization
  - [ ] Begin drafting questionnaire (don't send yet)

#### Week 2: Platform Functionality (8-10 to 8-15)
- **8-10-2025**: 
  - [ ] Improve benchmarks.html with better navigation and search
  - [ ] Add filtering by topic/category functionality
  - [ ] Test download functionality for all benchmarks

- **8-12-2025**: 
  - [ ] Complete user guide with comprehensive examples
  - [ ] Add benchmark usage tutorials and screenshots
  - [ ] Create troubleshooting section in user guide

- **8-15-2025**: 
  - [ ] Deploy benchmark platform to GitHub Pages
  - [ ] Test all core functionality end-to-end
  - [ ] Create project README with clear setup instructions

#### Week 3: Polish and Styling (8-17 to 8-22)
- **8-17-2025**: 
  - [ ] Complete CSS styling improvements for all pages
  - [ ] Fix UI/UX issues with collapsible panels
  - [ ] Add responsive design for mobile devices

- **8-20-2025**: 
  - [ ] Implement basic algorithm submission form structure
  - [ ] Create algorithms.html page layout (without backend)
  - [ ] Add form validation for future use

- **8-22-2025**: 
  - [ ] Final testing and bug fixes
  - [ ] Create comprehensive documentation
  - [ ] Prepare platform for initial user feedback

### Phase 2: Content Expansion & Community (September 2025)
**Target Completion: September 15, 2025**

- **8-25-2025**: 
  - [ ] Analyze questionnaire responses and prioritize benchmarks
  - [ ] Add 3-4 new benchmarks based on researcher feedback
  - [ ] Create standardized benchmark template

- **9-1-2025**: 
  - [ ] Add first Optimal Transport benchmark
  - [ ] Add first Mean Field Control benchmark
  - [ ] Implement benchmark categorization and tagging

- **9-8-2025**: 
  - [ ] Create benchmark submission workflow for researchers
  - [ ] Add benchmark validation checklist
  - [ ] Implement basic search and filter functionality

- **9-15-2025**: 
  - [ ] Launch beta version with 8-10 benchmarks across categories
  - [ ] Send to initial group of researchers for feedback
  - [ ] Create feedback collection system

### Phase 3: Automation & Algorithm Integration (October 2025)
**Target Completion: October 15, 2025**

- **9-20-2025**: 
  - [ ] Set up GitHub Actions for algorithm validation
  - [ ] Create template repository for algorithm submissions
  - [ ] Implement basic result storage system

- **10-1-2025**: 
  - [ ] Launch algorithm submission functionality
  - [ ] Create basic leaderboard system
  - [ ] Add algorithm comparison visualizations

- **10-15-2025**: 
  - [ ] Full platform launch with automation
  - [ ] Community outreach and promotion
  - [ ] Gather feedback for future improvements

### Success Metrics by Phase
- **Phase 1**: 5+ quality benchmarks, functional download system, positive initial feedback
- **Phase 2**: 8-10 benchmarks, researcher engagement, standardized submission process  
- **Phase 3**: Automated workflows, 5+ algorithm submissions, active community

### Immediate Priorities (Next 2 Weeks)
1. **Core benchmarks**: Focus on creating 4-5 high-quality, well-documented benchmarks
2. **User experience**: Ensure smooth benchmark discovery and download process
3. **Documentation**: Complete user guide with clear examples
4. **Community**: Send questionnaire to gather more benchmark requirements

### Dependencies & Risks
- **Critical**: Researcher questionnaire responses for benchmark priorities
- **Technical**: GitHub Pages deployment and file hosting
- **Content**: Expert validation of benchmark implementations
- **Timeline**: Buffer 20% extra time for each milestone