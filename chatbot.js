// static/js/chatbot.js
import responses from './chatbot_responses.js';

document.addEventListener("DOMContentLoaded", () => {
  const chatbotBtn = document.getElementById("chatbot-btn");
  const chatbotBox = document.getElementById("chatbot-box");
  const closeBtn = document.getElementById("close-chatbot");
  const sendBtn = document.getElementById("send-msg");
  const userInput = document.getElementById("user-input");
  const chatMessages = document.getElementById("chat-messages");

  // Open Chatbot
  chatbotBtn.addEventListener("click", () => {
    chatbotBox.style.display = "flex";
    userInput.focus();
  });
  

  // Close Chatbot
  closeBtn.addEventListener("click", () => {
    chatbotBox.style.display = "none";
  });

  // Send message (on Enter)
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  // Send message (on click)
  sendBtn.addEventListener("click", () => {
    sendMessage();
  });

  function sendMessage() {
    const userMsg = userInput.value.trim();
    if (userMsg === "") return;

    appendMessage("You", userMsg, "user");
    userInput.value = "";

    // Get bot reply
    const botReply = getBotReply(userMsg);
    setTimeout(() => {
      appendMessage("DVS Bot", botReply, "bot");
    }, 500);
  }

  function appendMessage(sender, message, type) {
    const msg = document.createElement("div");
    msg.className = `message ${type}`;
    msg.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
  }

  function getBotReply(msg) {
    const text = msg.toLowerCase();
    return responses[text] || "🤖 Sorry, I didn’t understand that. Can you rephrase?";
  }
});
