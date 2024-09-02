// Utility function to format date and time
function formatDateTime(dateTimeString) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    const dateTime = new Date(dateTimeString);
    return dateTime.toLocaleString('en-US', options);
}

// Utility function to display notifications
function displayNotifications(data) {
    const notifications = [];
    const now = new Date().toISOString();

    data.forEach(product => {
        if (product.stock < product.threshold) {
            const notification = `${product.name} stock is low. Current stock: ${product.stock}, Threshold: ${product.threshold}`;
            notifications.push(notification);
            addToLog(notification, now);
        }
    });

    if (notifications.length > 0) {
        showNotification(notifications.join('<br>'));
    } else {
        showNotification('No products are low on stock.');
    }
}

// Function to add notification to log
function addToLog(notification, dateTime) {
    let log = JSON.parse(localStorage.getItem('notificationLog')) || [];
    log.unshift({ message: notification, time: dateTime }); // Add new notifications to the beginning

    // Limit the number of logs to prevent excessive growth
    if (log.length > 100) {
        log = log.slice(0, 100);
    }

    localStorage.setItem('notificationLog', JSON.stringify(log));
    updateLogDisplay();
}

// Function to update log display
function updateLogDisplay() {
    const logList = document.getElementById('log-list');
    const log = JSON.parse(localStorage.getItem('notificationLog')) || [];
    logList.innerHTML = ''; // Clear previous logs
    log.forEach(entry => {
        const li = document.createElement('li');
        li.textContent = `${formatDateTime(entry.time)}: ${entry.message}`; // Include time in log
        logList.appendChild(li);
    });
}

// Function to show notification on the page
function showNotification(message) {
    const notification = document.getElementById('notification');
    const messageDiv = document.getElementById('message');
    const closeBtn = document.querySelector('.notification .close-btn');
    
    messageDiv.innerHTML = message;
    notification.style.display = 'block';
    closeBtn.style.display = 'block'; // Show the close button
}

// Function to hide notification
function closeNotification() {
    document.getElementById('notification').style.display = 'none';
    document.querySelector('.notification .close-btn').style.display = 'none'; // Hide the close button
}

// Function to load and handle the default CSV file
function loadDefaultCSV() {
    fetch('products.csv')
        .then(response => response.text())
        .then(csvText => {
            const lines = csvText.split('\n').filter(line => line.trim() !== ''); // Filter out empty lines
            const headers = lines[0].split(',');
            const data = lines.slice(1).map(line => {
                const values = line.split(',');
                if (values.length === headers.length) {
                    return {
                        name: values[0],
                        stock: parseInt(values[1], 10),
                        threshold: parseInt(values[2], 10)
                    };
                } else {
                    // Handle or log invalid line
                    console.warn('Skipping invalid line:', line);
                    return null;
                }
            }).filter(item => item !== null); // Remove null entries
            displayNotifications(data);
        })
        .catch(error => {
            console.error('Error loading the default CSV:', error);
            showNotification('Error loading default CSV file.');
        });
}

// Event listener for clearing notifications
document.getElementById('clearNotificationLog').addEventListener('click', function() {
    document.getElementById('notification').style.display = 'none';
    document.querySelector('.notification .close-btn').style.display = 'none'; // Hide the close button
    localStorage.removeItem('notificationLog');
    updateLogDisplay();
});

// Update log display and load default CSV on page load
document.addEventListener('DOMContentLoaded', function() {
    updateLogDisplay();
    loadDefaultCSV(); // Automatically load notifications on page load
});
