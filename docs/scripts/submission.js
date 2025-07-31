// Toggle visibility of submission fields based on the selected type
function toggleSubmissionFields() {
    const submissionType = document.getElementById("submission-type").value;

    // Get all submission fields
    const resultsField = document.getElementById("results-field");
    const githubField = document.getElementById("github-field");
    const codeField = document.getElementById("code-field");

    // Hide all fields initially
    resultsField.style.display = "none";
    githubField.style.display = "none";
    codeField.style.display = "none";

    // Show the selected field
    if (submissionType === "results") {
        resultsField.style.display = "block";
    } else if (submissionType === "github") {
        githubField.style.display = "block";
    } else if (submissionType === "code") {
        codeField.style.display = "block";
    }
}

// Handle form submission
document.getElementById("submission-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    const submissionType = document.getElementById("submission-type").value;

    if (submissionType === "results") {
        const resultsFile = document.getElementById("results-file").files[0];
        if (resultsFile) {
            alert(`Results file "${resultsFile.name}" submitted successfully!`);
        } else {
            alert("Please upload a results file.");
        }
    } else if (submissionType === "github") {
        const githubLink = document.getElementById("github-link").value;
        if (githubLink) {
            alert(`GitHub link "${githubLink}" submitted successfully!`);
        } else {
            alert("Please enter a GitHub repository link.");
        }
    } else if (submissionType === "code") {
        const codeFile = document.getElementById("code-files").files[0];
        if (codeFile) {
            alert(`Code file "${codeFile.name}" submitted successfully!`);
        } else {
            alert("Please upload a code file.");
        }
    }
});