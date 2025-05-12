export function scrollToElementSmoothly(id, offset = 750, duration = 600) {
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

// Main setup function
export function setupBudgetFormToggle() {
  document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.getElementById("show-budget-form");
    const editLink = document.getElementById("edit-budget-plan");
    const formBlock = document.getElementById("budget-form-container");

    // Toggle budget form
    function toggleForm(e) {
      e.preventDefault();
      if (formBlock) {
        formBlock.style.display = "block";
      }
      if (addBtn) addBtn.style.display = "none";
    }

    if (addBtn) addBtn.addEventListener("click", toggleForm);
    if (editLink) editLink.addEventListener("click", toggleForm);

    // Frequency switcher (AJAX chart + table update)
    const frequencyButtons = document.querySelectorAll("#frequency-toggle-group .tool-button");
    const chartContainer = document.getElementById("budget-planner-results");
    const summaryTableBody = document.querySelector("table tbody");

    frequencyButtons.forEach(button => {
      button.addEventListener("click", async function (e) {
        e.preventDefault();

        const selectedFreq = this.dataset.frequency;

        // Update button styling
        frequencyButtons.forEach(btn => btn.classList.remove("active"));
        this.classList.add("active");

        try {
          const res = await fetch(`/budget-planner/view/${selectedFreq}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
          });

          const data = await res.json();
          if (data.error) {
            alert(data.error);
            return;
          }

          // Update table
          if (summaryTableBody) {
            summaryTableBody.innerHTML = "";
            data.summary.forEach(item => {
              const row = document.createElement("tr");
              row.className = item.status === "Over" ? "text-danger" : "text-success";
              row.innerHTML = `
                <td>${item.category}</td>
                <td>$${item.limit}</td>
                <td>$${item.spent}</td>
                <td>$${item.remaining}</td>
                <td>${item.status}</td>
              `;
              summaryTableBody.appendChild(row);
            });
          }

          // Update chart
          if (chartContainer) {
            Plotly.newPlot(chartContainer, data.plot_data, data.plot_layout);
          }

        } catch (error) {
          console.error("Failed to fetch frequency data:", error);
        }
      });
    });

    // Scroll to target if specified
    const scrollTarget = document.body.dataset.scrollTargetId;
    if (scrollTarget) {
      scrollToElementSmoothly(scrollTarget);
    }
  });
}