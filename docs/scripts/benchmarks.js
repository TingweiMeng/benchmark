// Define problems for each category
const problems = {
    hj_pde: [
        { title: "HJ PDE Problem 1", description: "Description of HJ PDE Problem 1" },
        { title: "HJ PDE Problem 2", description: "Description of HJ PDE Problem 2" },
    ],
    optimal_control: [
        { title: "Optimal Control Problem 1", description: "Description of Optimal Control Problem 1" },
        { title: "Optimal Control Problem 2", description: "Description of Optimal Control Problem 2" },
    ],
    ot: [
        { title: "Optimal Transport Problem 1", description: "Description of Optimal Transport Problem 1" },
        { title: "Optimal Transport Problem 2", description: "Description of Optimal Transport Problem 2" },
    ],
    mfc: [
        { title: "Mean-Field Control Problem 1", description: "Description of Mean-Field Control Problem 1" },
        { title: "Mean-Field Control Problem 2", description: "Description of Mean-Field Control Problem 2" },
    ],
    jko: [
        { title: "JKO Problem 1", description: "Description of JKO Problem 1" },
        { title: "JKO Problem 2", description: "Description of JKO Problem 2" },
    ],
};

// Function to display problems for a selected category
function showProblems(category) {
    const problemsList = document.getElementById("problems-list");
    problemsList.innerHTML = ""; // Clear previous content

    if (problems[category]) {
        problems[category].forEach(problem => {
            const problemDiv = document.createElement("div");
            problemDiv.classList.add("problem");

            const title = document.createElement("h3");
            title.textContent = problem.title;

            const description = document.createElement("p");
            description.textContent = problem.description;

            problemDiv.appendChild(title);
            problemDiv.appendChild(description);
            problemsList.appendChild(problemDiv);
        });
    } else {
        problemsList.innerHTML = "<p>No problems available for this category.</p>";
    }
}


// Toggle collapsible panels
document.addEventListener("DOMContentLoaded", function () {
  const collapsibles = document.querySelectorAll(".collapsible");
  
  collapsibles.forEach(function(collapsible) {
      collapsible.addEventListener("click", function() {
          // Toggle active class
          this.classList.toggle("active");
          
          // Get the content panel
          const content = this.nextElementSibling;
          
          // Toggle content visibility
          if (content.classList.contains("active")) {
              content.classList.remove("active");
          } else {
              content.classList.add("active");
          }
      });
  });
});

// Show problems based on category
function showProblems(category) {
  const problemsList = document.getElementById("problems-list");
  
  // Clear existing content
  problemsList.innerHTML = "";
  
  if (category === 'hj_pde') {
      problemsList.innerHTML = `
          <div class="problem-category">
              <button class="collapsible">HJ PDE - Whole Domain</button>
              <div class="collapsible-content">
                  <div class="collapsible-inner">
                      <h4>Problems with Unbounded or Whole Domain</h4>
                      <p>Hamilton-Jacobi equations solved on unbounded domains or the whole space.</p>
                      
                      <!-- Burgers' Equation -->
                      <button class="collapsible">Burgers' Equation</button>
                      <div class="collapsible-content">
                          <div class="collapsible-inner">
                              <p><strong>Description:</strong> The Burgers' equation is a fundamental PDE in fluid mechanics and nonlinear acoustics.</p>
                              <p><strong>Equation:</strong></p>
                              <pre>∂u/∂t + u ∂u/∂x = ν ∂²u/∂x²</pre>
                              <p><strong>Initial Condition:</strong> u(x, 0) = -sin(πx), x ∈ [0, 1]</p>
                              <p><strong>Boundary Conditions:</strong> Periodic boundary conditions</p>
                              
                              <div class="benchmark-links">
                                  <a href="../../benchmarks/HJ/HJ_wholedomain/burgers_details.md" target="_blank">📖 View Full Details</a>
                                  <button class="download-btn" onclick="downloadBenchmark('burgers')">💾 Download Benchmark Code</button>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
          
          <div class="problem-category">
              <button class="collapsible">HJ PDE - Periodic Boundary Conditions</button>
              <div class="collapsible-content">
                  <div class="collapsible-inner">
                      <h4>Problems with Periodic Boundary Conditions</h4>
                      <p>Hamilton-Jacobi equations with periodic boundary conditions.</p>
                      <p><em>Benchmarks coming soon...</em></p>
                  </div>
              </div>
          </div>
          
          <div class="problem-category">
              <button class="collapsible">HJ PDE - Dirichlet Boundary Conditions</button>
              <div class="collapsible-content">
                  <div class="collapsible-inner">
                      <h4>Problems with Dirichlet Boundary Conditions</h4>
                      <p>Hamilton-Jacobi equations with Dirichlet boundary conditions.</p>
                      <p><em>Benchmarks coming soon...</em></p>
                  </div>
              </div>
          </div>
      `;
      
      // Re-initialize collapsible functionality for new content
      initializeCollapsibles();
  }
  
  // Add other categories here
  else if (category === 'optimal_control') {
      problemsList.innerHTML = `
          <div class="problem-category">
              <p><em>Optimal Control benchmarks coming soon...</em></p>
          </div>
      `;
  }
  else if (category === 'optimal_transport') {
      problemsList.innerHTML = `
          <div class="problem-category">
              <p><em>Optimal Transport benchmarks coming soon...</em></p>
          </div>
      `;
  }
  else if (category === 'mean_field') {
      problemsList.innerHTML = `
          <div class="problem-category">
              <p><em>Mean Field Control benchmarks coming soon...</em></p>
          </div>
      `;
  }
}

// Initialize collapsible functionality
function initializeCollapsibles() {
  const collapsibles = document.querySelectorAll(".collapsible");
  
  collapsibles.forEach(function(collapsible) {
      // Remove existing event listeners to avoid duplicates
      collapsible.replaceWith(collapsible.cloneNode(true));
  });
  
  // Re-add event listeners
  const newCollapsibles = document.querySelectorAll(".collapsible");
  newCollapsibles.forEach(function(collapsible) {
      collapsible.addEventListener("click", function() {
          this.classList.toggle("active");
          const content = this.nextElementSibling;
          if (content && content.classList.contains("collapsible-content")) {
              content.classList.toggle("active");
          }
      });
  });
}

// Download benchmark code
function downloadBenchmark(problem) {
  const downloadLinks = {
      burgers: "../../benchmarks/HJ/HJ_wholedomain/burgers.py",
      // Add more benchmarks here as they become available
  };

  if (downloadLinks[problem]) {
      // Create a temporary link element to trigger download
      const link = document.createElement('a');
      link.href = downloadLinks[problem];
      link.download = downloadLinks[problem].split('/').pop(); // Extract filename
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
  } else {
      alert("Benchmark code not available yet. Please check back soon!");
  }
}

// View benchmark details
function viewDetails(problem) {
  const detailsLinks = {
      burgers: "../benchmarks/HJ/HJ_wholedomain/burgers_details.md",
      // Add more detail links here
  };
  
  if (detailsLinks[problem]) {
      window.open(detailsLinks[problem], '_blank');
  } else {
      alert("Details not available yet.");
  }
}