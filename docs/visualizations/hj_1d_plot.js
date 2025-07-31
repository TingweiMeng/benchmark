document.addEventListener("DOMContentLoaded", function () {
    const data = [
        {
            x: ["Solver A", "Solver B", "Solver C"],
            y: [0.1, 0.2, 0.15],
            type: "bar",
            name: "Error",
        },
    ];

    const layout = {
        title: "HJ 1D Benchmark Results",
        xaxis: { title: "Solver" },
        yaxis: { title: "Error" },
    };

    Plotly.newPlot("visualization", data, layout);
});