const themeToggle = document.querySelector('.theme-toggle');
const body = document.body;
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.querySelector('.message-input');
const sendButton = document.querySelector('.send-button');
const typingIndicator = document.querySelector('.typing-indicator');

const generateShortUniqueId = () => Math.random().toString(36).substring(2, 8);

let isDarkTheme = false;
themeToggle.addEventListener('click', () => {
    isDarkTheme = !isDarkTheme;
    body.setAttribute('data-theme', isDarkTheme ? 'dark' : 'light');
    themeToggle.innerHTML = isDarkTheme ?
        '<i class="fas fa-sun"></i>' :
        '<i class="fas fa-moon"></i>';
});

function createMessageElement(id, content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.innerHTML = `
        <div class="avatar">${isUser ? 'U' : 'AI'}</div>
        <div class="message-bubble">${content}</div>
    `;
    messageDiv.id = id;
    return messageDiv;
}

function addMessage(id, content, isUser = false) {
    const element = document.getElementById(id);
    if (element) {
      element.querySelector('.message-bubble').innerHTML += content;
    } else {
      const messageElement = createMessageElement(id, content, isUser);
      chatContainer.appendChild(messageElement);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function handleSendMessage() {
  ws.send(JSON.stringify({
    id: generateShortUniqueId(),
    role: 'user',
    content: messageInput.value.trim(),
  }));
  messageInput.value = '';
}

const ws = new WebSocket("ws://localhost:8000/ws");
ws.onopen = (event) => console.log('Connection opened', event);
ws.onclose = (event) => console.log('Connection closed', event);

ws.onmessage = (event) => {
  /**
   * @type {Object}
   * @property {string} status
   * @property {string} role
   * @property {string} userMsgId
   * @property {string} userMsg
   * @property {string} assistantMsgId
   * @property {string} assistantMsg
   */
  const parsed = JSON.parse(event.data);

  if (parsed.status === 'msg-received') {
    addMessage(parsed.userMsgId, parsed.userMsg, true);
    showTypingIndicator()
  } else if (parsed.status === 'end') {
    hideTypingIndicator();
  } else if (parsed.status === 'response-stream') {
    hideTypingIndicator();
    addMessage(parsed.assistantMsgId, parsed.assistantMsg, false);
  } else if (parsed.status === 'error') {
    console.log(parsed.status, parsed);
  } else {
    console.log(parsed.status, parsed);
  }
};

sendButton.addEventListener('click', handleSendMessage);
messageInput.addEventListener('keypress', (e) => (e.key === 'Enter') && handleSendMessage());