// Function to load and display CSV data
function loadAndDisplayCSV() {
  fetch('inventory.csv')
      .then(response => response.text())
      .then(csvText => {
          const lines = csvText.split('\n').filter(line => line.trim() !== '');
          const headers = lines[0].split(',');
          const tbody = document.querySelector('#recent-orders--table tbody');
          tbody.innerHTML = ''; // Clear existing rows

          lines.slice(1).forEach(line => {
              const values = line.split(',');
              const row = document.createElement('tr');
              values.forEach(value => {
                  const cell = document.createElement('td');
                  cell.textContent = value;
                  row.appendChild(cell);
              });
              tbody.appendChild(row);
          });
      })
      .catch(error => {
          console.error('Error loading the CSV file:', error);
      });
}

// Load the CSV data when the page loads
document.addEventListener('DOMContentLoaded', loadAndDisplayCSV);
