/* Ollie Teaching Mode's real, shared "Ask Ollie" widget -- ROADMAP.md
 * Phase 1, item 3. Any Lab page includes this one script (plus
 * ollie-widget.css) to get a consistent Ask Ollie action, instead of
 * building its own chat window. A Lab can set `window.OLLIE_CONTEXT`
 * before or after this script loads -- re-read fresh on every message
 * send, not cached once, so a Lab whose state changes (e.g. Math Lab's
 * current quiz question) can keep it live.
 */
(function () {
  const fab = document.createElement("button");
  fab.type = "button";
  fab.className = "ollie-fab";
  fab.innerHTML = "🤖 Ask Ollie";
  document.body.appendChild(fab);

  const overlay = document.createElement("div");
  overlay.className = "ollie-overlay";
  overlay.hidden = true;
  overlay.innerHTML =
    '<div class="ollie-panel">' +
    '<div class="ollie-header"><span>🤖 Ask Ollie</span><button type="button" class="ollie-close" aria-label="Close">✕</button></div>' +
    '<div class="ollie-messages"></div>' +
    '<form class="ollie-input-row"><input type="text" placeholder="Ask Ollie anything..." autocomplete="off"><button type="submit">Send</button></form>' +
    "</div>";
  document.body.appendChild(overlay);

  const messagesEl = overlay.querySelector(".ollie-messages");
  const form = overlay.querySelector("form");
  const input = overlay.querySelector("input");
  const closeBtn = overlay.querySelector(".ollie-close");

  let history = [];

  function open() {
    overlay.hidden = false;
    input.focus();
  }
  function close() {
    overlay.hidden = true;
  }

  function addMessage(role, text) {
    const bubble = document.createElement("div");
    bubble.className = "ollie-bubble ollie-bubble-" + role;
    bubble.textContent = text;
    messagesEl.appendChild(bubble);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return bubble;
  }

  async function sendMessage(message) {
    addMessage("user", message);
    history.push({ role: "user", content: message });
    const bubble = addMessage("assistant", "");
    bubble.classList.add("ollie-bubble-typing");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: message,
          history: history.slice(0, -1),
          context: window.OLLIE_CONTEXT || null,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(function () { return {}; });
        bubble.textContent = data.error || "Something went wrong.";
        bubble.classList.remove("ollie-bubble-typing");
        bubble.classList.add("ollie-bubble-error");
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let full = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        full += decoder.decode(value, { stream: true });
        bubble.textContent = full;
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }
      bubble.classList.remove("ollie-bubble-typing");
      history.push({ role: "assistant", content: full });
    } catch (err) {
      bubble.textContent = "Couldn't reach Ollie right now.";
      bubble.classList.remove("ollie-bubble-typing");
      bubble.classList.add("ollie-bubble-error");
    }
  }

  fab.addEventListener("click", open);
  closeBtn.addEventListener("click", close);
  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) close();
  });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    input.value = "";
    sendMessage(message);
  });
})();
