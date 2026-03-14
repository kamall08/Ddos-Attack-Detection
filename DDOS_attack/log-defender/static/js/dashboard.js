document.addEventListener('DOMContentLoaded', () => {
    // 1. Interactive file upload label logic (if on index page)
    const fileInput = document.getElementById('file');
    const fileLabel = document.querySelector('.file-label span');
    
    if (fileInput && fileLabel) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                fileLabel.textContent = e.target.files[0].name;
                fileLabel.style.color = 'var(--text-primary)';
            } else {
                fileLabel.textContent = 'Select a server log file (.txt, .log)';
                fileLabel.style.color = 'var(--text-secondary)';
            }
        });
    }

    // 2. Chart rendering logic (if on dashboard page)
    const chartDataElement = document.getElementById('chart-data');
    if (chartDataElement) {
        try {
            const chartData = JSON.parse(chartDataElement.textContent);
            renderChart(chartData);
        } catch (e) {
            console.error("Error parsing chart data: ", e);
        }
    }
});

function renderChart(data) {
    const ctx = document.getElementById('trafficChart');
    if (!ctx) return;

    // Chart.js dark theme defaults
    Chart.defaults.color = '#a0a5b8';
    Chart.defaults.borderColor = 'rgba(45, 51, 72, 0.5)';

    // Determine colors based on thresholds.
    // If a request count is > 100, make the bar red, otherwise blue.
    const backgroundColors = data.data.map(val => 
        val > 100 ? 'rgba(239, 68, 68, 0.8)' : 'rgba(59, 130, 246, 0.8)'
    );
    const borderColors = data.data.map(val => 
        val > 100 ? 'rgb(239, 68, 68)' : 'rgb(59, 130, 246)'
    );

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Requests per IP',
                data: data.data,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 33, 48, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#a0a5b8',
                    borderColor: '#2d3348',
                    borderWidth: 1,
                    padding: 10,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.parsed.y + ' requests';
                            if (context.parsed.y > 100) {
                                label += ' (Suspicious)';
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(45, 51, 72, 0.5)',
                        drawBorder: false,
                    },
                    ticks: {
                        font: {
                            family: "'Inter', sans-serif"
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: "'Inter', sans-serif"
                        },
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            }
        }
    });
}
