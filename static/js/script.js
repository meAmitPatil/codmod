let finalCode = ""; // Store the final refined code globally for execution

async function sendModificationRequest() {
    const initialCode = document.getElementById('initial_code').value;
    const modificationRequest = document.getElementById('modification_request').value;

    // Show loading indicator
    document.getElementById('loading').style.display = 'block';
    document.getElementById('error_message').style.display = 'none'; // Hide error message
    document.getElementById('success_message').style.display = 'none'; // Hide success message

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

        // Update the Final Code section
        finalCode = result.generated_code;
        document.getElementById('generated_code').textContent = finalCode;

        // Display success message
        document.getElementById('success_message').textContent = "Final code generated successfully!";
        document.getElementById('success_message').style.display = 'block';

        // Add final code to the chat box
        addChatEntry(`You: ${modificationRequest}`, true);
        addChatEntry(`Final Code:\n${finalCode}`);
    } catch (error) {
        // Handle errors
        console.error("Error:", error.message);
        document.getElementById('error_message').textContent = error.message;
        document.getElementById('error_message').style.display = 'block';
    } finally {
        // Hide loading indicator
        document.getElementById('loading').style.display = 'none';
    }
}

async function executeCode() {
    if (!finalCode) {
        alert("No final code available to execute. Please generate the code first.");
        return;
    }

    // Show loading indicator
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

        // Update the execution result sections
        document.getElementById('stdout_output').textContent = result.stdout || "No output generated";
        document.getElementById('stderr_output').textContent = result.stderr || "No errors";

        // Display success message
        document.getElementById('success_message').textContent = "Code executed successfully!";
        document.getElementById('success_message').style.display = 'block';
    } catch (error) {
        // Handle errors
        console.error("Error:", error.message);
        document.getElementById('error_message').textContent = error.message;
        document.getElementById('error_message').style.display = 'block';
    } finally {
        // Hide loading indicator
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
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
}
