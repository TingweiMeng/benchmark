// Load benchmark names for the selected category from benchmark_data.json
let benchmarkData = null;

async function fetchBenchmarkData() {
    if (benchmarkData) return benchmarkData;
    try {
        const resp = await fetch('benchmark_data.json');
        benchmarkData = await resp.json();
    } catch (e) {
        benchmarkData = { categories: {} };
    }
    return benchmarkData;
}

async function loadBenchmarkNames() {
    const category = document.getElementById('solution-category').value;
    const select = document.getElementById('solution-benchmark');
    select.innerHTML = '<option value="">-- Select Benchmark --</option>';

    if (!category) return;

    const data = await fetchBenchmarkData();
    const benchmarks = (data.categories || {})[category] || [];
    benchmarks.forEach(b => {
        const opt = document.createElement('option');
        opt.value = b.name;
        opt.textContent = b.name;
        select.appendChild(opt);
    });

    if (benchmarks.length === 0) {
        select.innerHTML = '<option value="">No benchmarks in this category</option>';
    }
}

// Toggle visibility of solution submission fields
function toggleSubmissionFields() {
    const submissionType = document.getElementById('submission-type').value;
    document.getElementById('results-field').style.display        = submissionType === 'results' ? 'block' : 'none';
    document.getElementById('solution-github-field').style.display = submissionType === 'github'  ? 'block' : 'none';
    document.getElementById('code-field').style.display           = submissionType === 'code'    ? 'block' : 'none';
}

// Toggle visibility of benchmark submission fields
function toggleBenchmarkFields() {
    const benchmarkType = document.getElementById('benchmark-type').value;
    document.getElementById('benchmark-github-field').style.display = benchmarkType === 'github' ? 'block' : 'none';
    document.getElementById('benchmark-file-field').style.display   = benchmarkType === 'file'   ? 'block' : 'none';
}

// Handle solution form submission
document.getElementById('submission-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const category  = document.getElementById('solution-category').value;
    const benchmark = document.getElementById('solution-benchmark').value;
    const type      = document.getElementById('submission-type').value;

    if (!category) { alert('Please select a benchmark category.'); return; }
    if (!benchmark) { alert('Please select a benchmark.'); return; }

    if (type === 'results') {
        const file = document.getElementById('results-file').files[0];
        if (!file) { alert('Please upload a results CSV file.'); return; }
        alert(`Results for "${benchmark}" (${category}) submitted: ${file.name}`);
    } else if (type === 'github') {
        const link = document.getElementById('solution-github-link').value;
        if (!link) { alert('Please enter a GitHub repository link.'); return; }
        alert(`Solution for "${benchmark}" (${category}) submitted: ${link}`);
    } else if (type === 'code') {
        const file = document.getElementById('code-files').files[0];
        if (!file) { alert('Please upload a code ZIP file.'); return; }
        alert(`Code for "${benchmark}" (${category}) submitted: ${file.name}`);
    }
});

// Handle benchmark form submission
document.getElementById('benchmark-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const category    = document.getElementById('benchmark-category').value;
    const name        = document.getElementById('benchmark-name').value;
    const description = document.getElementById('benchmark-description').value;
    const type        = document.getElementById('benchmark-type').value;

    if (!category) { alert('Please select a category.'); return; }
    if (!name)     { alert('Please enter a benchmark name.'); return; }

    if (type === 'github') {
        const link = document.getElementById('benchmark-github-link').value;
        if (!link) { alert('Please enter a GitHub repository link.'); return; }
        alert(`Benchmark "${name}" (${category}) submitted with GitHub link: ${link}`);
    } else if (type === 'file') {
        const file = document.getElementById('benchmark-files').files[0];
        if (!file) { alert('Please upload a benchmark ZIP file.'); return; }
        alert(`Benchmark "${name}" (${category}) submitted with file: ${file.name}`);
    }
});
