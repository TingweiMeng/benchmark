// Define problems for each category
const problems = {
    hjb_pde: [
        { title: "HJB PDE Problem 1", description: "Description of HJB PDE Problem 1" },
        { title: "HJB PDE Problem 2", description: "Description of HJB PDE Problem 2" },
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
// ...existing code...

// Show problems based on category
function showProblems(category) {
  const problemsList = document.getElementById("problems-list");
  
  // Clear existing content
  problemsList.innerHTML = "";
  
  if (category === 'hjb_pde') {
      problemsList.innerHTML = `
          <div class="problem-category">
              <button class="collapsible">HJB PDE - Whole Domain</button>
              <div class="collapsible-content">
                  <div class="collapsible-inner">
                      <h4>Problems with Unbounded or Whole Domain</h4>
                      <p>Hamilton-Jacobi-Bellman equations solved on unbounded domains or the whole space.</p>
                      
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
                                  <button class="details-btn" onclick="toggleDetails('burgers')">📖 View Full Details</button>
                                  <button class="download-btn" onclick="downloadBenchmark('burgers')">💾 Download Benchmark Code</button>
                              </div>
                              
                              <!-- Details Panel -->
                              <div id="burgers-details" class="details-panel" style="display: none;">
                                  <div class="details-content">
                                      <h4>📖 Burgers' Equation - Full Details</h4>
                                      <div class="details-section">
                                          <h5>Problem Overview</h5>
                                          <p>The Burgers' equation is a simplified form of the Navier-Stokes equations that captures the essential nonlinear dynamics while remaining analytically tractable. It serves as an important test case for numerical methods.</p>
                                      </div>
                                      
                                      <div class="details-section">
                                          <h5>Mathematical Formulation</h5>
                                          <p><strong>PDE:</strong></p>
                                          <pre>∂u/∂t + u ∂u/∂x = ν ∂²u/∂x²</pre>
                                          <p>where:</p>
                                          <ul>
                                              <li>u(x,t) is the velocity field</li>
                                              <li>ν is the kinematic viscosity</li>
                                              <li>x ∈ [0, 1] is the spatial domain</li>
                                              <li>t > 0 is time</li>
                                          </ul>
                                      </div>
                                      
                                      <div class="details-section">
                                          <h5>Initial and Boundary Conditions</h5>
                                          <p><strong>Initial Condition:</strong></p>
                                          <pre>u(x, 0) = -sin(πx), x ∈ [0, 1]</pre>
                                          <p><strong>Boundary Conditions:</strong> Periodic boundary conditions</p>
                                          <pre>u(0, t) = u(1, t)
∂u/∂x|_{x=0} = ∂u/∂x|_{x=1}</pre>
                                      </div>
                                      
                                      <div class="details-section">
                                          <h5>Numerical Parameters</h5>
                                          <ul>
                                              <li>Viscosity: ν = 0.01</li>
                                              <li>Domain: x ∈ [0, 1]</li>
                                              <li>Time interval: t ∈ [0, 1]</li>
                                              <li>Grid points: 256</li>
                                              <li>Time steps: 1000</li>
                                          </ul>
                                      </div>
                                      
                                      <div class="details-section">
                                          <h5>Expected Behavior</h5>
                                          <p>The solution exhibits shock formation due to the nonlinear convection term, followed by viscous smoothing. The initial sinusoidal profile steepens and eventually develops into a smooth traveling wave.</p>
                                      </div>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
          
          <div class="problem-category">
              <button class="collapsible">HJB PDE - Periodic Boundary Conditions</button>
              <div class="collapsible-content">
                  <div class="collapsible-inner">
                      <h4>Problems with Periodic Boundary Conditions</h4>
                      <p>Hamilton-Jacobi-Bellman equations with periodic boundary conditions.</p>
                      <p><em>Benchmarks coming soon...</em></p>
                  </div>
              </div>
          </div>
          
          <div class="problem-category">
              <button class="collapsible">HJB PDE - Dirichlet Boundary Conditions</button>
              <div class="collapsible-content">
                  <div class="collapsible-inner">
                      <h4>Problems with Dirichlet Boundary Conditions</h4>
                      <p>Hamilton-Jacobi-Bellman equations with Dirichlet boundary conditions.</p>
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
      burgers: "../../benchmarks/HJB/HJB_wholedomain/burgers_benchmark.py",
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

// Toggle details panel
function toggleDetails(problem) {
  const detailsPanel = document.getElementById(`${problem}-details`);
  const button = event.target;
  
  if (detailsPanel.style.display === 'none') {
      detailsPanel.style.display = 'block';
      button.textContent = '📖 Hide Details';
      detailsPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } else {
      detailsPanel.style.display = 'none';
      button.textContent = '📖 View Full Details';
  }
}