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

export function scrollToElementSmoothly(id, offset = 150, duration = 600) {
    const target = document.getElementById(id);
    if (!target) return;
  
    const targetY = target.getBoundingClientRect().top + window.pageYOffset - offset;
    const startY = window.scrollY;
    const distance = targetY - startY;
    let startTime = null;
  
    function easeInOutQuad(t) {
      return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }
  
    function animateScroll(currentTime) {
      if (!startTime) startTime = currentTime;
      const timeElapsed = currentTime - startTime;
      const progress = easeInOutQuad(Math.min(timeElapsed / duration, 1));
      window.scrollTo(0, startY + distance * progress);
      if (timeElapsed < duration) {
        requestAnimationFrame(animateScroll);
      }
    }
  
    requestAnimationFrame(animateScroll);
  }
  