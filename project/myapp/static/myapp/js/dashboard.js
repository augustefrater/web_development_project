window.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById('statusChart');
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['OK', 'Warning', 'Fault'],
        datasets: [{
          data: [12, 3, 5],
          backgroundColor: ['green', 'orange', 'red']
        }]
      }
    });
  
    document.getElementById("searchInput").addEventListener("input", function () {
      const val = this.value.toLowerCase();
      // Simulate filter
      document.getElementById("machineList").innerHTML = `Searching for "${val}"...`;
    });
  });

    // Chart initialization
    document.addEventListener('DOMContentLoaded', function() {
      const ctx = document.getElementById('statusChart').getContext('2d');
      
      const labels = ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'];
      
      const onlineData = [32, 35, 38, 36, 37, 39, 40, 38, 36];
      const maintenanceData = [10, 8, 6, 8, 6, 5, 4, 6, 7];
      const offlineData = [6, 5, 4, 4, 5, 4, 4, 4, 5];
      
      const chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Online',
              data: onlineData,
              borderColor: '#4ade80',
              backgroundColor: 'rgba(74, 222, 128, 0.1)',
              tension: 0.3,
              fill: true
            },
            {
              label: 'Maintenance',
              data: maintenanceData,
              borderColor: '#facc15',
              backgroundColor: 'rgba(250, 204, 21, 0.1)',
              tension: 0.3,
              fill: true
            },
            {
              label: 'Offline',
              data: offlineData,
              borderColor: '#f87171',
              backgroundColor: 'rgba(248, 113, 113, 0.1)',
              tension: 0.3,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              align: 'end',
              labels: {
                boxWidth: 12,
                usePointStyle: true,
                pointStyle: 'circle'
              }
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              backgroundColor: 'rgba(255, 255, 255, 0.9)',
              titleColor: '#333',
              bodyColor: '#666',
              borderColor: '#e0e0e0',
              borderWidth: 1,
              padding: 10,
              displayColors: true,
              boxWidth: 8,
              boxHeight: 8,
              usePointStyle: true,
              callbacks: {
                title: function(tooltipItems) {
                  return tooltipItems[0].label;
                }
              }
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            }
          }
        }
      });
      
      // Search functionality
      const searchInput = document.getElementById('searchInput');
      const machineItems = document.querySelectorAll('.machine-item');
      
      searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        machineItems.forEach(item => {
          const machineName = item.querySelector('.machine-name').textContent.toLowerCase();
          const machineDetails = item.querySelector('.machine-details').textContent.toLowerCase();
          
          if (machineName.includes(searchTerm) || machineDetails.includes(searchTerm)) {
            item.style.display = 'flex';
          } else {
            item.style.display = 'none';
          }
        });
      });
      
      // Add click handlers for chart buttons
      const chartBtns = document.querySelectorAll('.chart-btn');
      chartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
          chartBtns.forEach(b => b.classList.remove('active'));
          this.classList.add('active');
          
          // In a real application, you would fetch new data and update the chart
          // This is just a simulation
          if (this.textContent === 'Week') {
            chart.data.labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            chart.data.datasets[0].data = [33, 35, 37, 39, 38, 36, 35];
            chart.data.datasets[1].data = [8, 7, 6, 5, 6, 7, 8];
            chart.data.datasets[2].data = [7, 6, 5, 4, 4, 5, 5];
          } else if (this.textContent === 'Month') {
            chart.data.labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
            chart.data.datasets[0].data = [34, 36, 38, 35];
            chart.data.datasets[1].data = [8, 7, 6, 9];
            chart.data.datasets[2].data = [6, 5, 4, 4];
          } else {
            chart.data.labels = ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'];
            chart.data.datasets[0].data = [32, 35, 38, 36, 37, 39, 40, 38, 36];
            chart.data.datasets[1].data = [10, 8, 6, 8, 6, 5, 4, 6, 7];
            chart.data.datasets[2].data = [6, 5, 4, 4, 5, 4, 4, 4, 5];
          }
          
          chart.update();
        });
      });
      
      // Refresh button click handler
      const refreshBtn = document.querySelector('.refresh-btn');
      refreshBtn.addEventListener('click', function() {
        // Simulate refresh with slight changes to data
        onlineData.push(onlineData.shift());
        maintenanceData.push(maintenanceData.shift());
        offlineData.push(offlineData.shift());
        
        chart.update();
        
        // Show feedback that refresh happened
        this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"></path></svg><span>Updated</span>';
        this.style.backgroundColor = 'rgba(74, 222, 128, 0.2)';
        this.style.borderColor = '#4ade80';
        this.style.color = '#16a34a';
        
        setTimeout(() => {
          this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path></svg><span>Refresh</span>';
          this.style.backgroundColor = '';
          this.style.borderColor = '';
          this.style.color = '';
        }, 2000);
      });
    });
