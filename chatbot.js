import { GoogleGenerativeAI } from "@google/generative-ai";

// Fetch your API_KEY
const API_KEY = "AIzaSyDV7AWgfuD1f3kke1aKDrGG-vRWlLr4Zzs";

document.addEventListener('DOMContentLoaded', () => {
    const genAI = new GoogleGenerativeAI(API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    const sendBtn = document.getElementById("send-btn");
    const speakBtn = document.getElementById("speak-btn");
    const stopBtn = document.getElementById("stop-btn");
    const userInput = document.getElementById("user-input");

    if (sendBtn) sendBtn.addEventListener("click", sendMessage);
    if (speakBtn) speakBtn.addEventListener("click", startRecognition);
    if (stopBtn) stopBtn.addEventListener("click", stopSpeech);
    if (userInput) {
        userInput.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                e.preventDefault(); // Prevent form submission if inside a form
                sendMessage();
            }
        });
    }

    const synth = window.speechSynthesis;

    function sendMessage() {
        const userInputValue = userInput.value.trim();
        if (!userInputValue) return;

        appendMessage("User", userInputValue);
        userInput.value = "";

        fetchReply(userInputValue);
    }

    function appendMessage(sender, message) {
        const chatBox = document.getElementById("chat-box");
        const messageElement = document.createElement("div");
        messageElement.className = "chat-message";

        let styledMessage = "";

        if (sender === "Bot" && message.includes("* ")) {
            const listItems = message
                .split("* ")
                .filter((item) => item.trim() !== "")
                .map((item) => `<li>${item.trim()}</li>`)
                .join("");

            styledMessage = `<strong>${sender}:</strong> <ul>${listItems}</ul>`;
        } else {
            styledMessage = `<strong>${sender}:</strong> <span class="preformatted">${message}</span>`;
        }

        messageElement.innerHTML = styledMessage;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function stopSpeech() {
        synth.cancel();
    }

    async function fetchReply(userInput) {
        try {
            let desiredText;

            // Check if the user's input is a greeting
            const lowerInput = userInput.trim().toLowerCase();
            if (lowerInput === "hi" || lowerInput === "hello" || lowerInput === "hii") {
                desiredText = "How can I help you today?";

                appendMessage("Bot", desiredText);
                return;
            }

            const result = await model.generateContent(userInput);
            const response = await result.response;
            desiredText = await response.text();

            if (!desiredText || desiredText.trim() === "") {
                desiredText = "Sorry, I didn't understand that. Could you please clarify?";
            }

            appendMessage("Bot", desiredText);

        } catch (error) {
            const errorMessage = "Sorry, I am having trouble connecting to the server.";
            appendMessage("Bot", errorMessage);
            console.error("Error:", error);
        }
    }

    function startRecognition() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.start();
        recognition.onresult = function (event) {
            const speechResult = event.results[0][0].transcript;
            userInput.value = speechResult;
            sendMessage();
        };
        recognition.onerror = function (event) {
            console.error("Recognition error:", event.error);
        };
    }
});
