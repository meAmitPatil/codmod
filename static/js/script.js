let finalCode = "";
async function sendModificationRequest() {
    const initialCode = document.getElementById('initial_code').value;
    const modificationRequest = document.getElementById('modification_request').value;

    document.getElementById('loading').style.display = 'block';
    document.getElementById('error_message').style.display = 'none'; 
    document.getElementById('success_message').style.display = 'none'; 

    try {
        const response = await fetch('/modify_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ initial_code: initialCode, modification_request: modificationRequest })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "An error occurred while modifying the code.");
        }

        const result = await response.json();

        addChatEntry(`AI: \n${result.generated_code}`);
    } catch (error) {
        console.error("Error:", error.message);
        document.getElementById('error_message').textContent = error.message;
        document.getElementById('error_message').style.display = 'block';
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function applyCode() {
    const chatBox = document.getElementById("chat-box");
    const aiResponses = chatBox.getElementsByClassName("ai-response");
    if (aiResponses.length === 0) {
        alert("No AI-generated code available to apply.");
        return;
    }

    const latestCode = aiResponses[aiResponses.length - 1].innerText;

    const codeBlockMatch = latestCode.match(/```python\s([\s\S]*?)```/);
    if (codeBlockMatch && codeBlockMatch[1]) {
        finalCode = codeBlockMatch[1].trim();
    } else {
        alert("No valid code block found in the AI response.");
        return;
    }

    document.getElementById("generated_code").textContent = finalCode;

    document.getElementById('success_message').textContent = "Code applied successfully!";
    document.getElementById('success_message').style.display = 'block';
}

async function executeCode() {
    if (!finalCode) {
        alert("No final code available to execute. Please generate the code first.");
        return;
    }

    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch('/run_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: finalCode })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "An error occurred while executing the code.");
        }

        const result = await response.json();

        document.getElementById('stdout_output').textContent = result.stdout || "No output generated";
        document.getElementById('stderr_output').textContent = result.stderr || "No errors";

        document.getElementById('success_message').textContent = "Code executed successfully!";
        document.getElementById('success_message').style.display = 'block';
    } catch (error) {
        console.error("Error:", error.message);
        document.getElementById('error_message').textContent = error.message;
        document.getElementById('error_message').style.display = 'block';
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
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
    chatBox.scrollTop = chatBox.scrollHeight;
}
