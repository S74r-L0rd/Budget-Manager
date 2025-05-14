document.addEventListener('DOMContentLoaded', function() {
    // check if chartCanvas exists
    const chartCanvas = document.getElementById('budgetChart');
    if (!chartCanvas) return;

    // get budget data from page
    const categoryElements = document.querySelectorAll('.category-item');
    if (categoryElements.length === 0) return;

    const labels = [];
    const data = [];
    const backgroundColors = [
        '#344E41', '#3A5A40', '#588157', '#A3B18A', '#DAD7CD',
        '#4A746A', '#5E8B7E', '#7D9D9C', '#9DC0BC', '#C2E0DE'
    ];

    // extract category and amount data
    categoryElements.forEach((element, index) => {
        const categoryName = element.querySelector('.category-name').textContent;
        const categoryValue = parseFloat(element.querySelector('.category-value').textContent.replace('$', ''));
        
        if (categoryValue > 0) {
            labels.push(categoryName);
            data.push(categoryValue);
        }
    });

    // create pie chart
    new Chart(chartCanvas, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors.slice(0, labels.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            size: 12
                        },
                        color: '#344E41'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: $${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
});