
// Chat WebSocket functionality
let currentChatSocket = null;

class ChatWebSocket {
    constructor(chatId, userName) {
        this.chatId = chatId;
        this.userName = userName;
        this.socket = null;
        this.messageContainer = document.querySelector('.messages-container');
        this.chatInput = document.querySelector('.chat-input input');
        this.sendButton = document.querySelector('.send-button');
        this.currentPage = 1;
        this.isLoading = false;
        this.hasMoreMessages = true;
        this.setupWebSocket();
        this.setupEventListeners();
    }

    setupWebSocket() {
        // Close existing socket if any
        if (currentChatSocket && currentChatSocket.socket) {
            currentChatSocket.socket.close();
        }

        this.socket = new WebSocket(`ws://168.231.127.170/ws/chat/${this.chatId}/`);
        currentChatSocket = this;
        
        this.socket.onopen = () => {
            console.log('WebSocket connection established');
            // Request initial messages
            this.loadMessages();
            // Update UI to show connection status
            this.updateConnectionStatus(true);
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'chat_message') {
                this.displayMessage(data, true);
            } else if (data.type === 'message_history') {
                this.handleMessageHistory(data.messages, data.has_more);
            }
        };

        this.socket.onclose = () => {
            console.log('WebSocket connection closed');
            this.updateConnectionStatus(false);
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus(false);
        };
    }

    updateConnectionStatus(connected) {
        const statusElement = document.querySelector('.status');
        if (statusElement) {
            statusElement.textContent = connected ? 'متصل' : 'غير متصل';
            statusElement.classList.toggle('online', connected);
        }
    }

    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Add scroll event listener for infinite scroll
        this.messageContainer.addEventListener('scroll', () => {
            if (this.shouldLoadMoreMessages()) {
                this.loadMessages();
            }
        });
    }

    shouldLoadMoreMessages() {
        if (this.isLoading || !this.hasMoreMessages) return false;
        
        const scrollTop = this.messageContainer.scrollTop;
        // Load more when user scrolls near the top (100px threshold)
        return scrollTop < 100;
    }

    loadMessages() {
        if (this.isLoading || !this.hasMoreMessages) return;
        
        this.isLoading = true;
        this.socket.send(JSON.stringify({
            'type': 'fetch_messages',
            'page': this.currentPage,
            'page_size': 20
        }));
    }

    handleMessageHistory(messages, hasMore) {
        const initialHeight = this.messageContainer.scrollHeight;
        const wasEmpty = this.messageContainer.children.length === 0;
        
        // Display messages at the top
        const fragment = document.createDocumentFragment();
        messages.reverse().forEach(message => {
            const messageElement = this.createMessageElement(message);
            fragment.appendChild(messageElement);
        });
        
        // Prepend messages if not the first load
        if (!wasEmpty) {
            this.messageContainer.insertBefore(fragment, this.messageContainer.firstChild);
            // Maintain scroll position
            const newHeight = this.messageContainer.scrollHeight;
            this.messageContainer.scrollTop = newHeight - initialHeight;
        } else {
            this.messageContainer.appendChild(fragment);
            this.scrollToBottom();
        }

        this.hasMoreMessages = hasMore;
        this.currentPage++;
        this.isLoading = false;
    }

    createMessageElement(data) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${data.sender == 1 ? 'sent' : 'received'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.textContent = data.message;
        
        messageContent.appendChild(messageText);
        messageDiv.appendChild(messageContent);

        return messageDiv;
    }

    displayMessage(data, isNew = false) {
        const messageElement = this.createMessageElement(data);
        
        if (isNew) {
            this.messageContainer.appendChild(messageElement);
            this.scrollToBottom();
        } else {
            this.messageContainer.insertBefore(messageElement, this.messageContainer.firstChild);
        }
    }

    sendMessage() {
        const message = this.chatInput.value.trim();
        if (message && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                'type': 'chat_message',
                'message': message
            }));
            this.chatInput.value = '';
        }
    }

    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
}

// Function to handle chat selection
function selectChat(element, chatId, userName) {
    // Update active chat styling
    document.querySelectorAll('.chat-item').forEach(item => {
        item.classList.remove('active');
    });
    element.classList.add('active');

    // Update chat header
    const chatHeader = document.querySelector('.current-chat-info h3');
    if (chatHeader) {
        chatHeader.textContent = userName;
    }

    // Initialize new WebSocket connection for selected chat
    new ChatWebSocket(chatId, userName);
}

// Initialize chat functionality when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        // Find first chat and select it if exists
        const firstChat = document.querySelector('.chat-item');
        if (firstChat) {
            const chatId = firstChat.getAttribute('data-chat-id');
            const userName = firstChat.querySelector('.chat-info h4').textContent;
            selectChat(firstChat, chatId, userName);
        }
    }
});