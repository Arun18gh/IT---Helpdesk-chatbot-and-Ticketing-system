window.addEventListener('DOMContentLoaded', () => {
  const deptLabels = Object.keys(deptData);
  const deptCounts = Object.values(deptData);

  const priorityLabels = Object.keys(priorityData);
  const priorityCounts = Object.values(priorityData);

  new Chart(document.getElementById('departmentChart'), {
    type: 'doughnut',
    data: {
      labels: deptLabels,
      datasets: [{
        label: 'Tickets by Department',
        data: deptCounts,
        backgroundColor: ['#00ffff', '#007bff', '#17a2b8', '#6610f2', '#28a745', '#ffc107']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: 'white' }
        }
      }
    }
  });

  new Chart(document.getElementById('priorityChart'), {
    type: 'doughnut',
    data: {
      labels: priorityLabels,
      datasets: [{
        label: 'Tickets by Priority',
        data: priorityCounts,
        backgroundColor: ['#ffc107', '#dc3545', '#28a745', '#00f7ff']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: 'white' }
        }
      }
    }
  });
});
