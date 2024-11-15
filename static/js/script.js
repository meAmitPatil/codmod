let modifiedCode = ""; // Store the modified code globally for execution

async function sendModificationRequest() {
    const initialCode = document.getElementById('initial_code').value;
    const modificationRequest = document.getElementById('modification_request').value;

    // Show loading indicator
    document.getElementById('loading').style.display = 'block';
    document.getElementById('error_message').style.display = 'none'; // Hide error message
    document.getElementById('success_message').style.display = 'none'; // Hide success message

    const response = await fetch('/modify_code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initial_code: initialCode, modification_request: modificationRequest })
    });
    const result = await response.json();

    // Hide loading indicator
    document.getElementById('loading').style.display = 'none';

    if (result.ai_response) {
        addChatEntry(`You: ${modificationRequest}`, true);
        addChatEntry(result.ai_response);  // Display AI response directly in the chat box

        // Store the modified code for execution
        modifiedCode = result.modified_code;
        document.getElementById('success_message').textContent = "Modification successful!";
        document.getElementById('success_message').style.display = 'block'; // Show success message
    } else {
        addChatEntry(`Error: ${result.error}`, true);
        document.getElementById('error_message').textContent = result.error; // Show error message
        document.getElementById('error_message').style.display = 'block'; // Show error message
    }
}

async function executeCode() {
    if (!modifiedCode) {
        alert("No modified code available to execute. Please request a modification first.");
        return;
    }

    // Show loading indicator
    document.getElementById('loading').style.display = 'block';

    const response = await fetch('/run_code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: modifiedCode })
    });
    const result = await response.json();

    // Hide loading indicator
    document.getElementById('loading').style.display = 'none';

    document.getElementById('stdout_output').textContent = result.stdout || "No output generated";
    document.getElementById('stderr_output').textContent = result.stderr || "No errors";
}

function addChatEntry(content, isUser = false) {
    const chatBox = document.getElementById("chat-box");
    const entry = document.createElement("div");
    entry.classList.add("chat-entry");

    if (!isUser) {
        entry.innerHTML = `<div class="ai-response"><pre>${content}</pre></div>`;
    } else {
        entry.innerHTML = `<div class="user-message">${content}</div>`;
    }

    chatBox.appendChild(entry);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message
}
