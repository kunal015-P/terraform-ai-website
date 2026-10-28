
const API_URL = "https://REPLACE_WITH_YOUR_API_URL"; // Replace

const form = document.querySelector("#chat-form");
const input = document.querySelector("#question");
const sendButton = document.querySelector("#send");
const messages = document.querySelector("#messages");
const warning = document.querySelector("#config-warning");

if (API_URL.startsWith("REPLACE_")) {
  warning.hidden = false;
}

function addMessage(text, type) {
  const message = document.createElement("div");

  message.className = `message ${type}`;
  message.textContent = text;

  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = input.value.trim();

  if (!question) return;

  if (API_URL.startsWith("REPLACE_")) {
    addMessage("Please configure the chatbot API URL first.", "error");
    return;
  }

  addMessage(question, "user");

  input.value = "";
  sendButton.disabled = true;
  sendButton.textContent = "Thinking...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Request failed");
    }

    addMessage(data.answer || "No answer received.", "assistant");
  } catch (error) {
    addMessage(
      `Unable to get a response: ${error.message}`,
      "error"
    );
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "Send ↗";
    input.focus();
  }
});
