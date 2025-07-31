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