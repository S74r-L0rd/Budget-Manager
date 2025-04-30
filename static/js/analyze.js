// Wait for DOM to fully load
document.addEventListener('DOMContentLoaded', function() {
    // Create spending pie chart
    createSpendingPieChart();
    
    // Create savings bar chart
    createSavingsBarChart();
});

// Create the spending breakdown pie chart
function createSpendingPieChart() {
    const ctx = document.getElementById('spending-pie-chart').getContext('2d');
    
    // Spending data
    const data = {
        labels: [
            'Home & utilities',
            'Insurance & financial',
            'Groceries',
            'Personal & medical',
            'Entertainment & eat-out',
            'Transport & auto',
            'Children'
        ],
        datasets: [{
            data: [87308, 167648, 3588, 0, 0, 0, 0],
            backgroundColor: [
                '#588157',  // Home & utilities - 深绿色
                '#344E41',  // Insurance & financial - 深橄榄绿色
                '#3A5A40',  // Groceries - 更深的绿色
                '#A3B18A',  // Personal & medical - 中绿色
                '#DAD7CD',  // Entertainment & eat-out - 浅灰绿色
                '#A3B18A',  // Transport & auto - 中绿色
                '#DAD7CD'   // Children - 浅灰绿色
            ],
            borderColor: '#ffffff',
            borderWidth: 2
        }]
    };
    
    // Chart configuration
    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            return `${label}: $${value.toLocaleString()}`;
                        }
                    }
                }
            },
            cutout: '0%', // Full pie chart, not donut
            radius: '90%',
            animation: {
                animateRotate: true,
                animateScale: true
            }
        }
    };
    
    // Create the chart
    new Chart(ctx, config);
}

// Create the savings bar chart
function createSavingsBarChart() {
    const ctx = document.getElementById('savings-bar-chart').getContext('2d');
    
    // Savings data for stacked bar chart with 3 segments
    const data = {
        labels: ['1'],
        datasets: [
            {
                label: 'Top Segment',
                data: [500],
                backgroundColor: '#DAD7CD', // 浅灰绿色
                borderColor: '#DAD7CD',
                borderWidth: 0,
                barPercentage: 0.6,
                categoryPercentage: 0.9
            },
            {
                label: 'Middle Segment',
                data: [4901],
                backgroundColor: '#588157', // 深绿色
                borderColor: '#588157',
                borderWidth: 0,
                barPercentage: 0.6,
                categoryPercentage: 0.9
            },
            {
                label: 'Bottom Segment',
                data: [2500],
                backgroundColor: '#344E41', // 深橄榄绿色
                borderColor: '#344E41',
                borderWidth: 0,
                barPercentage: 0.6,
                categoryPercentage: 0.9
            }
        ]
    };
    
    // Chart configuration
    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'x',
            scales: {
                y: {
                    stacked: true,
                    beginAtZero: true,
                    max: 8000,
                    grid: {
                        display: true,
                        color: '#e5e5e5',
                        lineWidth: 1
                    },
                    ticks: {
                        callback: function(value) {
                            if (value === 0) return '0';
                            if (value === 2500) return '2.5k';
                            if (value === 5000) return '5k';
                            if (value === 7500) return '7.5k';
                            return '';
                        },
                        padding: 10,
                        color: '#666',
                        font: {
                            family: 'Arial'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Savings',
                        color: '#666',
                        font: {
                            family: 'Arial',
                            size: 12
                        },
                        padding: {top: 10, bottom: 10}
                    },
                    border: {
                        display: false
                    }
                },
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#666',
                        font: {
                            family: 'Arial'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Years',
                        color: '#666',
                        font: {
                            family: 'Arial',
                            size: 12
                        },
                        padding: {top: 10, bottom: 0}
                    },
                    border: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false // Disable tooltips on hover
                }
            },
            layout: {
                padding: {
                    top: 20,
                    right: 20,
                    bottom: 20,
                    left: 20
                }
            }
        }
    };
    
    // Create the chart
    new Chart(ctx, config);
}
