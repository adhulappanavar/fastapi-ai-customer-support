// Web UI JavaScript for AI Customer Support
class CustomerSupportUI {
    constructor() {
        this.apiBaseUrl = 'http://localhost:7777';
        this.ticketingApiUrl = 'http://localhost:8000';
        this.workflowId = 'rag-customer-support-resolution-pipeline';
        this.chatMessages = [];
        this.isProcessing = false;
        this.tickets = [];
        this.filteredTickets = [];
        
        this.initializeEventListeners();
        this.checkApiStatus();
        this.checkTicketingApiStatus();
    }

    initializeEventListeners() {
        // Chat form submission
        const chatForm = document.getElementById('chatForm');
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => this.handleChatSubmit(e));
        }

        // Message input handling
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleChatSubmit(e);
                }
            });
        }

        // Ticket search input handling
        const ticketSearchInput = document.getElementById('ticketSearchInput');
        if (ticketSearchInput) {
            ticketSearchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.searchTickets();
                }
            });
        }
    }

    async checkApiStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/status`);
            if (response.ok) {
                this.updateStatusBadge(true);
                console.log('✅ AI API is online');
            } else {
                this.updateStatusBadge(false);
                console.log('❌ AI API is offline');
            }
        } catch (error) {
            this.updateStatusBadge(false);
            console.log('❌ Cannot connect to AI API:', error);
        }
    }

    async checkTicketingApiStatus() {
        try {
            const response = await fetch(`${this.ticketingApiUrl}/health`);
            if (response.ok) {
                this.updateTicketingApiStatus(true);
                console.log('✅ Ticketing API is online');
                // Load tickets if API is available
                this.loadTickets();
                this.loadTicketStats();
            } else {
                this.updateTicketingApiStatus(false);
                console.log('❌ Ticketing API is offline');
            }
        } catch (error) {
            this.updateTicketingApiStatus(false);
            console.log('❌ Cannot connect to Ticketing API:', error);
        }
    }

    updateStatusBadge(isOnline) {
        const statusBadge = document.querySelector('.status-badge');
        if (statusBadge) {
            if (isOnline) {
                statusBadge.className = 'status-badge online';
                statusBadge.innerHTML = '<i class="fas fa-circle"></i> AI Agent Online';
            } else {
                statusBadge.className = 'status-badge offline';
                statusBadge.innerHTML = '<i class="fas fa-circle"></i> AI Agent Offline';
            }
        }
    }

    updateTicketingApiStatus(isOnline) {
        const ticketingApiStatus = document.getElementById('ticketingApiStatus');
        if (ticketingApiStatus) {
            if (isOnline) {
                ticketingApiStatus.className = 'status-value online';
                ticketingApiStatus.textContent = 'Online';
            } else {
                ticketingApiStatus.className = 'status-value offline';
                ticketingApiStatus.textContent = 'Offline';
            }
        }
    }

    setQuery(query) {
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.value = query;
            this.showChat();
        }
    }

    showWelcome() {
        this.hideAllInterfaces();
        const welcomeSection = document.getElementById('welcomeSection');
        if (welcomeSection) {
            welcomeSection.style.display = 'block';
        }
        this.updateNavigationTabs('home');
    }

    showChat() {
        this.hideAllInterfaces();
        const chatInterface = document.getElementById('chatInterface');
        if (chatInterface) {
            chatInterface.style.display = 'flex';
            // Focus on input
            const messageInput = document.getElementById('messageInput');
            if (messageInput) {
                messageInput.focus();
            }
        }
        this.updateNavigationTabs('chat');
    }

    showTicketing() {
        console.log('🎫 showTicketing() called');
        this.hideAllInterfaces();
        const ticketingInterface = document.getElementById('ticketingInterface');
        console.log('🎫 ticketingInterface element:', ticketingInterface);
        if (ticketingInterface) {
            ticketingInterface.style.display = 'flex';
            console.log('🎫 Ticketing interface shown');
        } else {
            console.error('🎫 ticketingInterface element not found!');
        }
        this.updateNavigationTabs('tickets');
    }

    hideAllInterfaces() {
        console.log('👁️ hideAllInterfaces() called');
        const welcomeSection = document.getElementById('welcomeSection');
        const chatInterface = document.getElementById('chatInterface');
        const ticketingInterface = document.getElementById('ticketingInterface');
        
        if (welcomeSection) welcomeSection.style.display = 'none';
        if (chatInterface) chatInterface.style.display = 'none';
        if (ticketingInterface) ticketingInterface.style.display = 'none';
        
        console.log('👁️ All interfaces hidden');
    }

    updateNavigationTabs(activeTab) {
        console.log('🧭 updateNavigationTabs() called with:', activeTab);
        const navTabs = document.querySelectorAll('.nav-tab');
        console.log('🧭 Found nav tabs:', navTabs.length);
        navTabs.forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Try different selectors to find the active tab
        let activeTabElement = document.querySelector(`.nav-tab[onclick*="${activeTab}"]`);
        if (!activeTabElement && activeTab === 'tickets') {
            activeTabElement = document.querySelector(`.nav-tab[onclick*="showTicketing"]`);
        }
        if (!activeTabElement && activeTab === 'home') {
            activeTabElement = document.querySelector(`.nav-tab[onclick*="showWelcome"]`);
        }
        if (!activeTabElement && activeTab === 'chat') {
            activeTabElement = document.querySelector(`.nav-tab[onclick*="showChat"]`);
        }
        
        console.log('🧭 Active tab element:', activeTabElement);
        if (activeTabElement) {
            activeTabElement.classList.add('active');
        }
    }

    async handleChatSubmit(event) {
        event.preventDefault();
        
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || this.isProcessing) return;
        
        // Add user message to chat
        this.addMessage('user', message);
        messageInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator(true);
        
        try {
            this.isProcessing = true;
            const response = await this.sendMessageToAPI(message);
            this.addMessage('ai', response);
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('ai', 'Sorry, I encountered an error while processing your request. Please try again or contact support if the issue persists.');
        } finally {
            this.isProcessing = false;
            this.showTypingIndicator(false);
        }
    }

    async sendMessageToAPI(message) {
        const formData = new FormData();
        formData.append('workflow_input', message);
        
        const response = await fetch(
            `${this.apiBaseUrl}/runs?workflow_id=${this.workflowId}`,
            {
                method: 'POST',
                body: formData
            }
        );
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        return data.content || 'No response content received';
    }

    addMessage(sender, content) {
        const message = {
            id: Date.now(),
            sender: sender,
            content: content,
            timestamp: new Date()
        };
        
        this.chatMessages.push(message);
        this.renderChatMessages();
        this.scrollToBottom();
    }

    renderChatMessages() {
        const chatMessagesContainer = document.getElementById('chatMessages');
        if (!chatMessagesContainer) return;
        
        chatMessagesContainer.innerHTML = this.chatMessages.map(message => 
            this.createMessageHTML(message)
        ).join('');
    }

    createMessageHTML(message) {
        const isUser = message.sender === 'user';
        const avatarIcon = isUser ? 'fas fa-user' : 'fas fa-robot';
        const timeString = message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        return `
            <div class="message ${message.sender}" data-message-id="${message.id}">
                <div class="message-avatar">
                    <i class="${avatarIcon}"></i>
                </div>
                <div class="message-content">
                    ${this.formatMessageContent(message.content)}
                    <div class="message-time">${timeString}</div>
                </div>
            </div>
        `;
    }

    formatMessageContent(content) {
        // Convert markdown-like content to HTML
        let formatted = content
            // Headers
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h4>$1</h4>')
            .replace(/^# (.*$)/gim, '<h5>$1</h5>')
            
            // Bold and italic
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            
            // Lists
            .replace(/^\d+\.\s+(.*$)/gim, '<li>$1</li>')
            .replace(/^-\s+(.*$)/gim, '<li>$1</li>')
            
            // Line breaks
            .replace(/\n/g, '<br>');
        
        // Wrap lists in ul tags
        if (formatted.includes('<li>')) {
            formatted = formatted.replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>');
        }
        
        return formatted;
    }

    showTypingIndicator(show) {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.style.display = show ? 'flex' : 'none';
        }
    }

    scrollToBottom() {
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Ticketing functionality
    async loadTickets() {
        try {
            this.showTicketsLoading(true);
            const response = await fetch(`${this.ticketingApiUrl}/tickets?limit=100`);
            
            if (response.ok) {
                this.tickets = await response.json();
                this.filteredTickets = [...this.tickets];
                this.renderTickets();
                this.updateTicketsCount();
            } else {
                console.error('Failed to load tickets:', response.status);
                this.showNoTickets();
            }
        } catch (error) {
            console.error('Error loading tickets:', error);
            this.showNoTickets();
        } finally {
            this.showTicketsLoading(false);
        }
    }

    async loadTicketStats() {
        try {
            const response = await fetch(`${this.ticketingApiUrl}/stats`);
            if (response.ok) {
                const stats = await response.json();
                this.updateTicketStats(stats);
            }
        } catch (error) {
            console.error('Error loading ticket stats:', error);
        }
    }

    updateTicketStats(stats) {
        const totalTicketsCount = document.getElementById('totalTicketsCount');
        const openTicketsCount = document.getElementById('openTicketsCount');
        
        if (totalTicketsCount) {
            totalTicketsCount.textContent = stats.total_tickets;
        }
        if (openTicketsCount) {
            openTicketsCount.textContent = stats.open_tickets;
        }
    }

    renderTickets() {
        const ticketsList = document.getElementById('ticketsList');
        if (!ticketsList) return;
        
        if (this.filteredTickets.length === 0) {
            this.showNoTickets();
            return;
        }
        
        ticketsList.innerHTML = this.filteredTickets.map(ticket => 
            this.createTicketHTML(ticket)
        ).join('');
    }

    createTicketHTML(ticket) {
        const statusClass = this.getStatusClass(ticket.status_name);
        const priorityClass = this.getPriorityClass(ticket.priority_name);
        const createdDate = new Date(ticket.created_at).toLocaleDateString();
        
        const tags = ticket.tags ? ticket.tags.split(',').map(tag => 
            `<span class="ticket-tag">${tag.trim()}</span>`
        ).join('') : '';
        
        return `
            <div class="ticket-item" onclick="window.customerSupportUI.viewTicket(${ticket.id})">
                <div class="ticket-header">
                    <span class="ticket-number">${ticket.ticket_number}</span>
                    <div class="ticket-status">
                        <span class="status-badge-ticket ${statusClass}">${ticket.status_name}</span>
                    </div>
                </div>
                
                <div class="ticket-title">${ticket.title}</div>
                <div class="ticket-description">${ticket.description}</div>
                
                <div class="ticket-meta">
                    <div class="ticket-meta-item">
                        <i class="fas fa-user"></i>
                        <span>${ticket.user_full_name}</span>
                    </div>
                    <div class="ticket-meta-item">
                        <i class="fas fa-folder"></i>
                        <span>${ticket.category_name}</span>
                    </div>
                    <div class="ticket-meta-item">
                        <i class="fas fa-calendar"></i>
                        <span>${createdDate}</span>
                    </div>
                    <span class="ticket-priority ${priorityClass}">${ticket.priority_name}</span>
                </div>
                
                ${tags ? `<div class="ticket-tags">${tags}</div>` : ''}
            </div>
        `;
    }

    getStatusClass(statusName) {
        const statusMap = {
            'Open': 'open',
            'In Progress': 'in-progress',
            'Waiting for Customer': 'waiting',
            'Resolved': 'resolved',
            'Closed': 'closed',
            'Escalated': 'escalated'
        };
        return statusMap[statusName] || 'open';
    }

    getPriorityClass(priorityName) {
        const priorityMap = {
            'Critical': 'critical',
            'High': 'high',
            'Medium': 'medium',
            'Low': 'low'
        };
        return priorityMap[priorityName] || 'medium';
    }

    async searchTickets() {
        const searchInput = document.getElementById('ticketSearchInput');
        const query = searchInput.value.trim();
        
        if (!query) {
            this.filteredTickets = [...this.tickets];
        } else {
            try {
                const response = await fetch(`${this.ticketingApiUrl}/search?query=${encodeURIComponent(query)}&limit=50`);
                if (response.ok) {
                    const searchResult = await response.json();
                    this.filteredTickets = searchResult.results;
                } else {
                    // Fallback to client-side search
                    this.filteredTickets = this.tickets.filter(ticket => 
                        ticket.title.toLowerCase().includes(query.toLowerCase()) ||
                        ticket.description.toLowerCase().includes(query.toLowerCase()) ||
                        (ticket.tags && ticket.tags.toLowerCase().includes(query.toLowerCase()))
                    );
                }
            } catch (error) {
                // Fallback to client-side search
                this.filteredTickets = this.tickets.filter(ticket => 
                    ticket.title.toLowerCase().includes(query.toLowerCase()) ||
                    ticket.description.toLowerCase().includes(query.toLowerCase()) ||
                    (ticket.tags && ticket.tags.toLowerCase().includes(query.toLowerCase()))
                );
            }
        }
        
        this.renderTickets();
        this.updateTicketsCount();
    }

    filterTickets() {
        const statusFilter = document.getElementById('statusFilter').value;
        const priorityFilter = document.getElementById('priorityFilter').value;
        const categoryFilter = document.getElementById('categoryFilter').value;
        
        this.filteredTickets = this.tickets.filter(ticket => {
            const statusMatch = !statusFilter || ticket.status_id.toString() === statusFilter;
            const priorityMatch = !priorityFilter || ticket.priority_id.toString() === priorityFilter;
            const categoryMatch = !categoryFilter || ticket.category_id.toString() === categoryFilter;
            
            return statusMatch && priorityMatch && categoryMatch;
        });
        
        this.renderTickets();
        this.updateTicketsCount();
    }

    updateTicketsCount() {
        const ticketsCount = document.getElementById('ticketsCount');
        if (ticketsCount) {
            ticketsCount.textContent = `${this.filteredTickets.length} of ${this.tickets.length} tickets`;
        }
    }

    showTicketsLoading(show) {
        const ticketsLoading = document.getElementById('ticketsLoading');
        const ticketsList = document.getElementById('ticketsList');
        const noTickets = document.getElementById('noTickets');
        
        if (ticketsLoading) ticketsLoading.style.display = show ? 'flex' : 'none';
        if (ticketsList) ticketsList.style.display = show ? 'none' : 'flex';
        if (noTickets) noTickets.style.display = 'none';
    }

    showNoTickets() {
        const ticketsList = document.getElementById('ticketsList');
        const noTickets = document.getElementById('noTickets');
        
        if (ticketsList) ticketsList.style.display = 'none';
        if (noTickets) noTickets.style.display = 'flex';
    }

    async refreshTickets() {
        await this.loadTickets();
        await this.loadTicketStats();
    }

    viewTicket(ticketId) {
        // For now, just log the ticket ID
        // In the future, this could open a detailed view modal
        console.log(`Viewing ticket: ${ticketId}`);
        // You could implement a modal or redirect to a detailed view
    }

    // Utility method for external calls
    static setQuery(query) {
        if (window.customerSupportUI) {
            window.customerSupportUI.setQuery(query);
        }
    }
}

// Initialize the UI when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.customerSupportUI = new CustomerSupportUI();
    
    // Make setQuery globally available for onclick handlers
    window.setQuery = (query) => {
        window.customerSupportUI.setQuery(query);
    };
    
    // Make ticketing functions globally available
    window.showWelcome = () => window.customerSupportUI.showWelcome();
    window.showChat = () => window.customerSupportUI.showChat();
    window.showTicketing = () => window.customerSupportUI.showTicketing();
    window.refreshTickets = () => window.customerSupportUI.refreshTickets();
    window.searchTickets = () => window.customerSupportUI.searchTickets();
    window.filterTickets = () => window.customerSupportUI.filterTickets();
    
    console.log('🚀 AI Customer Support UI initialized with ticketing support');
});

// Add some interactive features
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects to feature items
    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = 'scale(1.05)';
        });
        item.addEventListener('mouseleave', () => {
            item.style.transform = 'scale(1)';
        });
    });

    // Add click effects to category items
    const categoryItems = document.querySelectorAll('.category-item');
    categoryItems.forEach(item => {
        item.addEventListener('click', () => {
            // Add a subtle click effect
            item.style.transform = 'scale(0.95)';
            setTimeout(() => {
                item.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Add smooth scrolling for better UX
    const smoothScroll = (target, duration) => {
        const targetPosition = target.getBoundingClientRect().top;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        let startTime = null;

        const animation = currentTime => {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const run = ease(timeElapsed, startPosition, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        };

        const ease = (t, b, c, d) => {
            t /= d / 2;
            if (t < 1) return c / 2 * t * t + b;
            t--;
            return -c / 2 * (t * (t - 2) - 1) + b;
        };

        requestAnimationFrame(animation);
    };

    // Add smooth scroll to example buttons
    const exampleButtons = document.querySelectorAll('.example-btn');
    exampleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const chatContainer = document.querySelector('.chat-container');
            if (chatContainer) {
                smoothScroll(chatContainer, 800);
            }
        });
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const sendBtn = document.getElementById('sendBtn');
        if (sendBtn && !sendBtn.disabled) {
            sendBtn.click();
        }
    }
    
    // Escape to go back to welcome
    if (e.key === 'Escape') {
        const chatInterface = document.getElementById('chatInterface');
        const ticketingInterface = document.getElementById('ticketingInterface');
        if (chatInterface && chatInterface.style.display !== 'none') {
            window.customerSupportUI.showWelcome();
        } else if (ticketingInterface && ticketingInterface.style.display !== 'none') {
            window.customerSupportUI.showWelcome();
        }
    }
});

// Add loading states and better error handling
class LoadingManager {
    static show(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.opacity = '0.6';
            element.style.pointerEvents = 'none';
        }
    }

    static hide(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.opacity = '1';
            element.style.pointerEvents = 'auto';
        }
    }
}

// Add toast notifications
class ToastManager {
    static show(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="fas fa-${this.getIcon(type)}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }

    static getIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Add toast styles dynamically
const toastStyles = `
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        z-index: 1000;
        max-width: 300px;
    }
    
    .toast.show {
        transform: translateX(0);
    }
    
    .toast-success { border-left: 4px solid #48bb78; }
    .toast-error { border-left: 4px solid #f56565; }
    .toast-warning { border-left: 4px solid #ed8936; }
    .toast-info { border-left: 4px solid #4299e1; }
    
    .toast i {
        font-size: 1.25rem;
    }
    
    .toast-success i { color: #48bb78; }
    .toast-error i { color: #f56565; }
    .toast-warning i { color: #ed8936; }
    .toast-info i { color: #4299e1; }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = toastStyles;
document.head.appendChild(styleSheet);
