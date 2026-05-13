const aiTrigger    = document.getElementById('aiTrigger');
const aiPanel      = document.getElementById('aiPanel');
const aiPanelClose = document.getElementById('aiPanelClose');
const aiMessages   = document.getElementById('aiMessages');
const aiInput      = document.getElementById('aiInput');
const aiSend       = document.getElementById('aiSend');

let chatHistory = [];
let isOpen = false;

// Toggle panel
function togglePanel() {
    isOpen = !isOpen;
    aiPanel.classList.toggle('open', isOpen);
    aiTrigger.classList.toggle('active', isOpen);
    if (isOpen) {
        aiInput.focus();
        scrollToBottom();
    }
}

aiTrigger.addEventListener('click', togglePanel);
aiPanelClose.addEventListener('click', togglePanel);

// Scroll la ultimul mesaj
function scrollToBottom() {
    aiMessages.scrollTop = aiMessages.scrollHeight;
}

// Adaugă mesaj în chat
function addMessage(content, role) {
    const div = document.createElement('div');
    div.className = `ai-msg ai-msg--${role === 'user' ? 'user' : 'bot'}`;
    div.innerHTML = `<div class="ai-msg-bubble">${content}</div>`;
    aiMessages.appendChild(div);
    scrollToBottom();
}

// Indicator "se scrie..."
function addTyping() {
    const div = document.createElement('div');
    div.className = 'ai-msg ai-msg--bot ai-typing';
    div.innerHTML = `
        <div class="ai-msg-bubble">
            <span></span><span></span><span></span>
        </div>`;
    aiMessages.appendChild(div);
    scrollToBottom();
    return div;
}

// Trimite mesaj
async function sendMessage() {
    const message = aiInput.value.trim();
    if (!message) return;

    aiInput.value = '';
    aiSend.disabled = true;
    addMessage(message, 'user');

    chatHistory.push({ role: 'user', content: message });

    const typingEl = addTyping();

    try {
        const res = await fetch('/ai/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrf(),
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory.slice(-10),
            })
        });

        const data = await res.json();
        typingEl.remove();

        if (data.response) {
            addMessage(data.response, 'bot');
            chatHistory.push({ role: 'model', content: data.response });
        } else if (data.error) {
            addMessage(`Eroare`, 'bot');  
        }

    } catch (err) {
        typingEl.remove();
        addMessage('Nu mă pot conecta. Verifică conexiunea.', 'bot');
    }

    aiSend.disabled = false;
    aiInput.focus();
}

aiSend.addEventListener('click', sendMessage);
aiInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function getCsrf() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
}