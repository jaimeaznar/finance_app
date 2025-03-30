// This would be included in your templates/index.html or as a separate JS file

// Store chat history for context
let chatHistory = [];

$(document).ready(function () {
    const chatForm = $('#chatForm');
    const messageInput = $('#messageInput');
    const chatMessages = $('#chatMessages');

    chatForm.on('submit', function (e) {
        e.preventDefault();

        const message = messageInput.val().trim();
        if (!message) return;

        // Add user message to chat
        appendMessage('user', message);

        // Add to history
        chatHistory.push({
            role: "user",
            content: message
        });

        // Clear input
        messageInput.val('');

        // Show typing indicator
        showTypingIndicator();

        // Call the API
        $.ajax({
            url: '/api/chat',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                message: message,
                history: chatHistory.slice(-10) // Send last 10 messages for context
            }),
            success: function (response) {
                // Remove typing indicator
                removeTypingIndicator();

                // Add AI response to chat
                appendMessage('ai', response.text);

                // Add to history
                chatHistory.push({
                    role: "assistant",
                    content: response.text
                });

                // Display recommendations if any
                if (response.recommendations && response.recommendations.length > 0) {
                    displayRecommendations(response.recommendations);
                }
            },
            error: function () {
                // Remove typing indicator
                removeTypingIndicator();

                // Show error message
                appendMessage('ai', "I'm sorry, I encountered an error processing your request. Please try again.");
            }
        });
    });

    function appendMessage(sender, content) {
        const messageClass = sender === 'user' ? 'message user' : 'message ai';
        const messageHTML = `
            <div class="${messageClass}">
                <div class="message-content">
                    <p>${content}</p>
                </div>
            </div>
        `;

        chatMessages.append(messageHTML);

        // Scroll to bottom
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    }

    function showTypingIndicator() {
        const typingHTML = `
            <div class="message ai typing">
                <div class="message-content">
                    <p>Thinking<span class="typing-dots">...</span></p>
                </div>
            </div>
        `;

        chatMessages.append(typingHTML);
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    }

    function removeTypingIndicator() {
        $('.typing').remove();
    }

    function displayRecommendations(recommendations) {
        // Clear previous recommendations
        $('#aiRecommendationsContainer').empty();

        // Add new recommendations
        recommendations.forEach(rec => {
            let iconClass = 'fa-chart-line text-primary';
            if (rec.type === 'revenue') iconClass = 'fa-dollar-sign text-success';
            if (rec.type === 'payment') iconClass = 'fa-exclamation-circle text-warning';
            if (rec.type === 'expense') iconClass = 'fa-money-bill-wave text-danger';
            if (rec.type === 'forecast') iconClass = 'fa-chart-bar text-info';

            const recHTML = `
                <div class="card recommendation-card ${rec.type} mb-3">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <i class="fas ${iconClass} mb-2"></i>
                                <h5 class="card-title">${rec.title}</h5>
                                <p class="card-text">${rec.description}</p>
                            </div>
                            <div class="text-end">
                                ${rec.potential ? `<div class="mb-2 text-success">+$${rec.potential}</div>` : ''}
                                ${rec.due_date ? `<div class="mb-2 text-warning">Due: ${rec.due_date}</div>` : ''}
                                <button class="btn btn-primary btn-sm">${rec.action}</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            $('#aiRecommendationsContainer').append(recHTML);
        });
    }
});

// Add this to your CSS or in a <style> tag
/*
.typing-dots {
    display: inline-block;
    width: 20px;
    text-align: left;
    animation: typing 1.5s infinite;
}

@keyframes typing {
    0% { content: '.'; }
    33% { content: '..'; }
    66% { content: '...'; }
    100% { content: '.'; }
}
*/
