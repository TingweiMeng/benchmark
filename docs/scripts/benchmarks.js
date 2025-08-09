// scripts/benchmarks.js

let benchmarkData = null;
let currentCategory = null;

// Load benchmark data when page loads
document.addEventListener('DOMContentLoaded', async function() {
    await loadBenchmarkData();
    generateCategoriesList();
    showAllBenchmarks(); // Show all by default
});

async function loadBenchmarkData() {
    try {
        const response = await fetch('benchmark_data.json');
        benchmarkData = await response.json();
        
        // Update summary
        updateSummary();
        
        // Hide loading
        document.getElementById('benchmarks-loading').style.display = 'none';
        document.getElementById('categories-loading').style.display = 'none';
        
    } catch (error) {
        console.error('Error loading benchmark data:', error);
        document.getElementById('benchmarks-loading').innerHTML = 'Error loading benchmarks. Please try again later.';
        document.getElementById('categories-loading').innerHTML = 'Error loading categories.';
    }
}

function updateSummary() {
    if (!benchmarkData) return;
    
    document.getElementById('total-categories').textContent = `${benchmarkData.summary.total_categories} Categories`;
    document.getElementById('total-benchmarks').textContent = `${benchmarkData.summary.total_benchmarks} Benchmarks`;
    document.getElementById('total-test-cases').textContent = `${benchmarkData.summary.total_test_cases} Test Cases`;
    document.getElementById('last-updated').textContent = `Last updated: ${new Date(benchmarkData.last_updated).toLocaleString()}`;
    document.getElementById('benchmark-summary').style.display = 'block';
}

function generateCategoriesList() {
    if (!benchmarkData) return;
    
    const categoriesList = document.getElementById('categories-list');
    categoriesList.innerHTML = '<h3>Categories</h3>';
    
    // Add "All" option
    const allButton = document.createElement('button');
    allButton.textContent = 'All Benchmarks';
    allButton.className = 'category-btn active';
    allButton.onclick = () => showAllBenchmarks();
    categoriesList.appendChild(allButton);
    
    // Add category buttons
    Object.keys(benchmarkData.categories).forEach(category => {
        const button = document.createElement('button');
        button.textContent = formatCategoryName(category);
        button.className = 'category-btn';
        button.onclick = () => showProblems(category);
        categoriesList.appendChild(button);
    });
}

function formatCategoryName(category) {
    return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function showAllBenchmarks() {
    if (!benchmarkData) return;
    
    currentCategory = null;
    updateActiveCategory('All Benchmarks');
    
    const problemsList = document.getElementById('problems-list');
    problemsList.innerHTML = '';
    
    // Show all benchmarks grouped by category
    Object.entries(benchmarkData.categories).forEach(([category, benchmarks]) => {
        const categorySection = document.createElement('div');
        categorySection.className = 'category-section';
        categorySection.innerHTML = `<h3>${formatCategoryName(category)}</h3>`;
        
        benchmarks.forEach(benchmark => {
            const benchmarkCard = createBenchmarkCard(benchmark);
            categorySection.appendChild(benchmarkCard);
        });
        
        problemsList.appendChild(categorySection);
    });
}

function showProblems(category) {
    if (!benchmarkData || !benchmarkData.categories[category]) return;
    
    currentCategory = category;
    updateActiveCategory(formatCategoryName(category));
    
    const problemsList = document.getElementById('problems-list');
    problemsList.innerHTML = '';
    
    const benchmarks = benchmarkData.categories[category];
    benchmarks.forEach(benchmark => {
        const benchmarkCard = createBenchmarkCard(benchmark);
        problemsList.appendChild(benchmarkCard);
    });
}

function updateActiveCategory(categoryName) {
    // Update active button
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent === categoryName) {
            btn.classList.add('active');
        }
    });
}

function createBenchmarkCard(benchmark) {
    const card = document.createElement('div');
    card.className = 'benchmark-card';
    
    // Generate test cases table
    const testCasesTable = benchmark.test_cases.map((testCase) => `
        <tr class="${testCase.physics_regime.toLowerCase()}-case">
            <td>${testCase.case_id}</td>
            <td>${testCase.dimension}D</td>
            <td>${testCase.point_details}</td>
            <td>${testCase.parameters.nu !== undefined ? testCase.parameters.nu : 'N/A'}</td>
            <td>${testCase.description}</td>
        </tr>
    `).join('');
    
    // Generate parameter badges
    const dimensionBadges = benchmark.parameter_variations.dimensions.map(d => 
        `<span class="badge">${d}D</span>`
    ).join('');
    
    const viscosityBadges = benchmark.parameter_variations.viscosity_values.map(nu => 
        `<span class="badge ${nu === 0 ? 'inviscid' : 'viscous'}">${nu === 0 ? 'Inviscid' : `ν=${nu}`}</span>`
    ).join('');
    
    card.innerHTML = `
        <div class="benchmark-header">
            <h4>${benchmark.name}</h4>
            <span class="category-badge">${formatCategoryName(benchmark.category)}</span>
            <button class="download-btn" onclick="downloadBenchmark('${benchmark.download_url}', '${benchmark.name}')">
                Download
            </button>
        </div>
        
        <div class="benchmark-description">
            <p>${benchmark.description}</p>
            ${benchmark.initial_condition ? `<p><strong>Initial condition:</strong> ${benchmark.initial_condition}</p>` : ''}
        </div>
        
        <div class="test-cases-section">
            <h5>Test Cases <span class="case-count">(${benchmark.total_cases} cases)</span></h5>
            <button class="toggle-details" onclick="toggleTestCases(this)">Show Details ▼</button>
            
            <div class="test-cases-table" style="display: none;">
                <table>
                    <thead>
                        <tr>
                            <th>Case</th>
                            <th>Dimension</th>
                            <th>Grid/Points</th>
                            <th>Viscosity (ν)</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${testCasesTable}
                    </tbody>
                </table>
            </div>
            
            <div class="parameter-summary">
                <div class="param-group">
                    <h6>Dimensions Tested</h6>
                    <div class="param-badges">${dimensionBadges}</div>
                </div>
                <div class="param-group">
                    <h6>Physics Regimes</h6>
                    <div class="param-badges">${viscosityBadges}</div>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

function toggleTestCases(button) {
    const table = button.parentElement.querySelector('.test-cases-table');
    const isVisible = table.style.display !== 'none';
    
    if (isVisible) {
        table.style.display = 'none';
        button.textContent = 'Show Details ▼';
    } else {
        table.style.display = 'block';
        button.textContent = 'Hide Details ▲';
    }
}

function downloadBenchmark(url, benchmarkName) {
    // You can implement actual download logic here
    // For now, just log or redirect
    console.log(`Downloading ${benchmarkName} from ${url}`);
    // window.location.href = url;
    alert(`Download functionality for ${benchmarkName} will be implemented soon!`);
}