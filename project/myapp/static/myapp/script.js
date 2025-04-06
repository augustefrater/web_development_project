// main.js
document.addEventListener('DOMContentLoaded', () => {
    // Fetch machine statuses for dashboard
    fetchMachineStatuses();

    // Setup form event listeners
    setupForms();

    // Initialize Chart.js for visualization (if Manager dashboard)
    if (document.getElementById('statusChart')) {
        initStatusChart();
    }
});

// Fetch machine statuses via AJAX
function fetchMachineStatuses() {
    fetch('/api/machines/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()  // For Django CSRF protection
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        const machineList = document.getElementById('machine-list');
        if (machineList) {
            machineList.innerHTML = ''; // Clear existing content
            data.forEach(machine => {
                const statusClass = getStatusClass(machine.status);
                const item = document.createElement('div');
                item.className = `machine-item ${statusClass}`;
                item.innerHTML = `
                    <h3>${machine.name}</h3>
                    <p>Status: <span class="${statusClass}">${machine.status}</span></p>
                    <p>Assigned: ${machine.assigned_users.join(', ')}</p>
                    <button onclick="viewMachineDetails(${machine.id})">View Details</button>
                `;
                machineList.appendChild(item);
            });
        }
    })
    .catch(error => console.error('Error fetching machines:', error));
}

// Status styling
function getStatusClass(status) {
    switch (status) {
        case 'OK': return 'status-ok';
        case 'Warning': return 'status-warning';
        case 'Fault': return 'status-fault';
        default: return '';
    }
}

// View machine details (drill-down for Managers)
function viewMachineDetails(machineId) {
    window.location.href = `/machines/${machineId}/`; // Navigate to detail page
}

// Form setup for fault/warning submission
function setupForms() {
    const faultForm = document.getElementById('fault-form');
    const warningForm = document.getElementById('warning-form');

    if (faultForm) {
        faultForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (validateFaultForm()) {
                submitFault();
            }
        });
    }

    if (warningForm) {
        warningForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (validateWarningForm()) {
                submitWarning();
            }
        });
    }
}

// Validate fault form
function validateFaultForm() {
    const notes = document.getElementById('fault-notes').value;
    const image = document.getElementById('fault-image').files[0];
    if (!notes.trim()) {
        alert('Please provide fault notes.');
        return false;
    }
    return true;
}

// Validate warning form
function validateWarningForm() {
    const warningText = document.getElementById('warning-text').value;
    if (!warningText.trim()) {
        alert('Please provide a warning description.');
        return false;
    }
    return true;
}

// Submit fault via AJAX
function submitFault() {
    const formData = new FormData();
    formData.append('notes', document.getElementById('fault-notes').value);
    formData.append('image', document.getElementById('fault-image').files[0]);
    formData.append('machine_id', document.getElementById('machine-id').value);

    fetch('/api/faults/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Fault reported successfully!');
            fetchMachineStatuses(); // Refresh dashboard
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error submitting fault:', error));
}

// Submit warning via AJAX
function submitWarning() {
    const warningText = document.getElementById('warning-text').value;
    const machineId = document.getElementById('machine-id').value;

    fetch('/api/warnings/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ machine_id: machineId, text: warningText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Warning added successfully!');
            fetchMachineStatuses();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error submitting warning:', error));
}

// Get CSRF token from cookie (for Django)
function getCSRFToken() {
    const name = 'csrftoken';
    const cookieValue = document.cookie.split(';')
        .map(c => c.trim())
        .find(c => c.startsWith(name + '='))
        ?.split('=')[1];
    return cookieValue || '';
}

// Initialize Chart.js for Manager dashboard
function initStatusChart() {
    fetch('/api/machines/summary/', {
        method: 'GET',
        headers: { 'X-CSRFToken': getCSRFToken() }
    })
    .then(response => response.json())
    .then(data => {
        const ctx = document.getElementById('statusChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['OK', 'Warning', 'Fault'],
                datasets: [{
                    data: [data.ok, data.warning, data.fault],
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'top' } }
            }
        });
    })
    .catch(error => console.error('Error fetching summary:', error));
}
