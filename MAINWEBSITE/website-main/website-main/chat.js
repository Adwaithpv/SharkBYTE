document.addEventListener('DOMContentLoaded', function() {
    // Create chat button
    const chatButton = document.createElement('button');
    chatButton.className = 'chat-button';
    chatButton.innerHTML = '💬';
    document.body.appendChild(chatButton);

    // Create chat modal
    const chatModal = document.createElement('div');
    chatModal.className = 'chat-modal';
    chatModal.innerHTML = `
        <div class="chat-header">
            <span>Medicine Inventory Assistant</span>
            <span class="chat-close">×</span>
        </div>
        <div class="chat-messages"></div>
        <div class="chat-input-container">
            <input type="text" class="chat-input" placeholder="Type your message...">
            <button class="chat-send">Send</button>
        </div>
    `;
    document.body.appendChild(chatModal);

    // Chat state
    let isChatOpen = false;

    // Toggle chat modal
    chatButton.addEventListener('click', () => {
        isChatOpen = !isChatOpen;
        chatModal.style.display = isChatOpen ? 'flex' : 'none';
    });

    // Close chat modal
    chatModal.querySelector('.chat-close').addEventListener('click', () => {
        isChatOpen = false;
        chatModal.style.display = 'none';
    });

    // Handle sending messages
    const sendButton = chatModal.querySelector('.chat-send');
    const inputField = chatModal.querySelector('.chat-input');
    const messagesContainer = chatModal.querySelector('.chat-messages');

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message bot-message error-message';
        errorDiv.textContent = message;
        messagesContainer.appendChild(errorDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function sendMessage() {
        const message = inputField.value.trim();
        if (message) {
            addMessage(message, true);
            inputField.value = '';

            // Show loading indicator
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message loading-message';
            loadingDiv.textContent = 'Thinking...';
            messagesContainer.appendChild(loadingDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

            // Send message to backend
            fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Remove loading indicator
                messagesContainer.removeChild(loadingDiv);
                addMessage(data.response);
            })
            .catch(error => {
                // Remove loading indicator
                messagesContainer.removeChild(loadingDiv);
                showError('Sorry, there was an error connecting to the chatbot. Please make sure the server is running and try again.');
                console.error('Error:', error);
            });
        }
    }

    sendButton.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}); 