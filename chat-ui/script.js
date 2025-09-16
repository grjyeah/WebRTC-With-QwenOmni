// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// Add a message to the chat
function addMessage(sender, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const senderDiv = document.createElement('div');
    senderDiv.className = `sender ${sender}`;
    senderDiv.textContent = sender === 'user' ? 'You' : 'ChatBot';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(senderDiv);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to the bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Simulate bot response
function getBotResponse(userMessage) {
    // Simple response logic - in a real app, this would call an API
    const responses = [
        "That's interesting! Tell me more.",
        "I understand. How can I help you with that?",
        "Thanks for sharing. Is there anything specific you'd like to know?",
        "I see. What else would you like to discuss?",
        "Got it. Do you have any other questions?",
        "That's a great point. What are your thoughts on this?",
        "I appreciate you sharing that with me.",
        "Interesting perspective. Can you elaborate on that?"
    ];
    
    // Simple keyword-based responses for demo purposes
    if (userMessage.toLowerCase().includes('hello') || userMessage.toLowerCase().includes('hi')) {
        return "Hello there! How can I assist you today?";
    }
    
    if (userMessage.toLowerCase().includes('help')) {
        return "I'm here to help! You can ask me anything, and I'll do my best to assist you.";
    }
    
    if (userMessage.toLowerCase().includes('thank')) {
        return "You're welcome! Is there anything else I can help with?";
    }
    
    // Random response for other messages
    const randomIndex = Math.floor(Math.random() * responses.length);
    return responses[randomIndex];
}

// Handle sending a message
function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        // Add user message
        addMessage('user', message);
        
        // Clear input
        messageInput.value = '';
        
        // Simulate bot thinking delay
        setTimeout(() => {
            const botResponse = getBotResponse(message);
            addMessage('bot', botResponse);
        }, 1000);
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Add initial messages for demo
document.addEventListener('DOMContentLoaded', () => {
    addMessage('bot', 'Hello! I\'m your chat assistant. How can I help you today?');
    
    // Add a few demo messages
    setTimeout(() => {
        addMessage('user', 'Hi there! I have a question about this chat interface.');
        setTimeout(() => {
            addMessage('bot', 'Of course! This is a real-time chat interface that displays messages as they are sent. Each message shows the sender on the left and the content on the right. The list updates automatically as new messages are exchanged.');
        }, 1000);
    }, 1000);
});