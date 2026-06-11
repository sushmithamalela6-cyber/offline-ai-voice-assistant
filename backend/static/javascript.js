const micButton = document.getElementById("micButton");
const chatBox = document.getElementById("chatBox");
const statusText = document.getElementById("status");
const wave = document.querySelector(".wave");

let isListening = false;

// Add Message
function addMessage(text, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");
    messageDiv.classList.add(sender);

    messageDiv.innerText = text;

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}

// ChatGPT Typing Animation
function typeMessage(text, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");
    messageDiv.classList.add(sender);

    chatBox.appendChild(messageDiv);

    let i = 0;

    const typing = setInterval(() => {

        if (i < text.length) {

            messageDiv.textContent += text[i];

            chatBox.scrollTop = chatBox.scrollHeight;

            i++;

        } else {

            clearInterval(typing);
        }

    }, 15);
}
// Mic Click
micButton.addEventListener("click", async () => {

    if (isListening) return;

    isListening = true;

    micButton.disabled = true;

    statusText.innerText = "🎙️ Listening...";
    wave.classList.add("active");

    try {

        const response = await fetch("/listen");

        const data = await response.json();

        console.log("Received:", data);

        // User Message
        if (data.user && data.user !== "No voice detected") {

            addMessage("🎙️ " + data.user, "user");
        }

        // Thinking Message
        const thinking = document.createElement("div");

        thinking.classList.add("message");
        thinking.classList.add("bot");

        thinking.innerText = "🤖 Thinking...";

        chatBox.appendChild(thinking);

        chatBox.scrollTop = chatBox.scrollHeight;

        setTimeout(() => {

            thinking.remove();

            typeMessage(data.reply, "bot");

        }, 1000);

        statusText.innerText = "🤖 Generating response...";

    } catch (error) {

        console.log(error);

        statusText.innerText = "❌ Connection Error";

    } finally {
        wave.classList.remove("active");

        setTimeout(() => {

            micButton.disabled = false;

            isListening = false;

            statusText.innerText = "Tell me how can I help you ?";

        }, 1500);
    }
});

// Stop Button
async function stopAssistant() {

    try {

        await fetch("/stop");

        statusText.innerText = "⛔ Voice Stopped";

    } catch (error) {

        console.log(error);
    }
}
function addSpeakButton(text, parentDiv){

    const btn = document.createElement("button");

    btn.innerHTML = "🔊";

    btn.classList.add("speak-btn");

    btn.onclick = async () => {

        await fetch("/speak",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                text:text
            })
        });

    };

    parentDiv.appendChild(btn);
}                     