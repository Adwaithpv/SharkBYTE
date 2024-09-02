// Function to load and handle the CSV file
function loadCSV() {
  fetch('data.csv')
      .then(response => response.text())
      .then(csvText => {
          const lines = csvText.split('\n').filter(line => line.trim() !== ''); // Filter out empty lines
          const headers = lines[0].split(','); // Read headers
          const data = lines.slice(1).map(line => {
              const values = line.split(',');
              if (values.length === headers.length) {
                  return {
                      productName: values[0],
                      productNumber: values[1],
                      payment: values[2],
                      status: values[3]
                  };
              } else {
                  console.warn('Skipping invalid line:', line);
                  return null;
              }
          }).filter(item => item !== null); // Remove null entries
          displayData(data);
      })
      .catch(error => {
          console.error('Error loading the CSV file:', error);
          document.getElementById('recent-orders--table').innerHTML = 'Error loading CSV file.';
      });
}

// Function to display data on the page
function displayData(data) {
  const tbody = document.querySelector('#recent-orders--table tbody');
  let html = '';
  data.forEach(row => {
      html += `<tr>
          <td>${row.productName}</td>
          <td>${row.productNumber}</td>
          <td>${row.payment}</td>
          <td>${row.status}</td>
      </tr>`;
  });
  tbody.innerHTML = html;
}

// Update data display on page load
document.addEventListener('DOMContentLoaded', function() {
  loadCSV(); // Automatically load data on page load
});
