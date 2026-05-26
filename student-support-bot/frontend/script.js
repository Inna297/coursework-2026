const chat = document.getElementById("chat");
const input = document.getElementById("message");
const themeToggle = document.getElementById("themeToggle");

// ---------- LOAD HISTORY ----------
window.onload = () => {
    const history = localStorage.getItem("chatHistory");

    if (history) {
        chat.innerHTML = history;
    }

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        document.documentElement.classList.add("dark");
        themeToggle.innerText = "🌙";
    }
};

// ---------- SAVE HISTORY ----------
function saveHistory() {
    localStorage.setItem("chatHistory", chat.innerHTML);
}

// ---------- ADD MESSAGE ----------
function addMessage(text, sender) {
    const div = document.createElement("div");

    div.classList.add("message");
    div.classList.add(sender);

    div.innerText = text;

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;

    saveHistory();
}

// ---------- SEND ----------
async function sendMessage() {
    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");

    input.value = "";

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/chat?message=${encodeURIComponent(text)}`
        );

        const data = await response.json();

        addMessage(data.reply, "bot");

    } catch {
        addMessage("Помилка сервера", "bot");
    }
}

// ---------- ENTER ----------
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});

// ---------- THEME ----------
themeToggle.addEventListener("click", () => {

    document.documentElement.classList.toggle("dark");

    const isDark =
        document.documentElement.classList.contains("dark");

    if (isDark) {
        themeToggle.innerText = "🌙";
        localStorage.setItem("theme", "dark");
    } else {
        themeToggle.innerText = "☀️";
        localStorage.setItem("theme", "light");
    }
});