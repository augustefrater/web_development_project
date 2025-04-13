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
  