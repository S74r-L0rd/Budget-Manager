document.addEventListener("DOMContentLoaded", function() {
    if (typeof barData !== "undefined" && typeof pieData !== "undefined") {
        // Plot the bar chart
        Plotly.newPlot('barChart', barData.data, barData.layout);

        // Plot the pie chart
        Plotly.newPlot('pieChart', pieData.data, pieData.layout);
    }
});

document.addEventListener("DOMContentLoaded", function() {
    if (barData && Object.keys(barData).length > 0) {
        Plotly.newPlot('barChart', barData.data, barData.layout);
    }
    if (pieData && Object.keys(pieData).length > 0) {
        Plotly.newPlot('pieChart', pieData.data, pieData.layout);
    }
});

document.addEventListener("DOMContentLoaded", function() {
    if (typeof barData !== "undefined" && Object.keys(barData).length > 0) {
        Plotly.newPlot('barChart', barData.data, barData.layout);
    } else {
        console.error("No valid bar chart data.");
    }

    if (typeof pieData !== "undefined" && Object.keys(pieData).length > 0) {
        Plotly.newPlot('pieChart', pieData.data, pieData.layout);
    } else {
        console.error("No valid pie chart data.");
    }
});