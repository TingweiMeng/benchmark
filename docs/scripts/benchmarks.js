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
    categoriesList.innerHTML = '';
    
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
        button.onclick = () => showCategory(category);
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

function showCategory(category) {
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
        <tr class="${testCase.physics_regime.toLowerCase().replace(/\s+/g, '-')}-case">
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
    
    // Generate physics regime badges
    const physicsRegimes = [...new Set(benchmark.test_cases.map(tc => tc.physics_regime))];
    const physicsBadges = physicsRegimes.map(regime => {
        const className = regime.toLowerCase().replace(/\s+/g, '-');
        return `<span class="badge ${className}">${regime}</span>`;
    }).join('');
    
    // Generate point type badges
    const pointTypes = benchmark.quick_stats.point_types || [];
    const pointBadges = pointTypes.map(type => 
        `<span class="badge point-${type.toLowerCase()}">${type}</span>`
    ).join('');
    
    card.innerHTML = `
        <div class="benchmark-header">
            <h4>${benchmark.name}</h4>
            <span class="category-badge">${formatCategoryName(benchmark.category)}</span>
            <button class="download-btn" onclick="downloadBenchmark('${benchmark.file_path}', '${benchmark.name}')">
                Download
            </button>
        </div>
        
        <div class="benchmark-description">
            <p>${benchmark.short_description}</p>
            <p><strong>Equation:</strong> ${benchmark.equation}</p>
            ${benchmark.initial_condition ? `<p><strong>Initial condition:</strong> ${benchmark.initial_condition}</p>` : ''}
            
            <!-- Quick Summary Badges -->
            <div class="quick-summary">
                <span class="summary-badge">${benchmark.quick_stats.total_cases} test cases</span>
                <span class="summary-badge">${benchmark.quick_stats.dimension_range}</span>
                ${pointBadges}
            </div>
        </div>
        
        <div class="detailed-info">
            <button class="expand-btn" onclick="toggleDetails(this)">
                <span>View Test Case Details</span>
                <span class="icon">▼</span>
            </button>
            
            <div class="details-content" style="display: none;">
                <!-- Testing Aspects Overview -->
                ${Object.keys(benchmark.testing_aspects).length > 0 ? `
                <div class="testing-overview">
                    <h5>What This Benchmark Tests</h5>
                    <div class="test-aspects">
                        ${Object.entries(benchmark.testing_aspects).map(([key, value]) => `
                            <div class="aspect">
                                <strong>${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong> ${value}
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : ''}
                
                <!-- Detailed Test Cases Table -->
                <div class="test-cases-table">
                    <h5>Complete Test Case Breakdown</h5>
                    <table>
                        <thead>
                            <tr>
                                <th>Case</th>
                                <th>Dimension</th>
                                <th>Point Setup</th>
                                <th>Viscosity (ν)</th>
                                <th>Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${testCasesTable}
                        </tbody>
                    </table>
                </div>
                
                <!-- Parameter Summary -->
                <div class="parameter-summary">
                    <div class="param-group">
                        <h6>Dimensions Tested</h6>
                        <div class="param-badges">${dimensionBadges}</div>
                    </div>
                    <div class="param-group">
                        <h6>Physics Regimes</h6>
                        <div class="param-badges">${physicsBadges}</div>
                    </div>
                    ${pointTypes.length > 0 ? `
                    <div class="param-group">
                        <h6>Point Generation Methods</h6>
                        <div class="param-badges">${pointBadges}</div>
                    </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    return card;
}

function toggleDetails(button) {
    const detailsContent = button.parentElement.querySelector('.details-content');
    const icon = button.querySelector('.icon');
    const isVisible = detailsContent.style.display !== 'none';
    
    if (isVisible) {
        detailsContent.style.display = 'none';
        icon.textContent = '▼';
        button.querySelector('span').textContent = 'View Test Case Details';
    } else {
        detailsContent.style.display = 'block';
        icon.textContent = '▲';
        button.querySelector('span').textContent = 'Hide Test Case Details';
    }
}

function downloadBenchmark(filePath, benchmarkName) {
    console.log('Debug - filePath:', filePath);
    console.log('Debug - benchmarkName:', benchmarkName);
    
    // Extract just the filename if filePath contains directories
    const fileName = filePath.split('/').pop();
    console.log('Debug - fileName:', fileName);
    
    // Construct the correct download URL
    const downloadUrl = `../benchmarks/HJB/HJB_wholedomain/${fileName}`;
    console.log('Debug - downloadUrl:', downloadUrl);
    
    // Create temporary link and trigger download
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log(`Downloaded ${benchmarkName}: ${fileName}`);
}