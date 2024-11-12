import streamlit as st
import uuid
from config import OPENAI_API_KEY, MEM0_API_KEY, E2B_API_KEY
from memory import initialize_memory_client, get_memory, add_to_memory
from ai_client import initialize_openai_client, get_ai_response
from code_executor import execute_code
from utils import extract_code

# Initialize clients
client = initialize_openai_client(OPENAI_API_KEY)
mem_client = initialize_memory_client(MEM0_API_KEY)
user_id = str(uuid.uuid4())

# Set Streamlit page config
st.set_page_config(page_title="AI-Powered Code Modifier Chat", page_icon=":robot:")

# Initialize session state variables
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []
if "initial_code" not in st.session_state:
    st.session_state["initial_code"] = ""
if "last_modified_code" not in st.session_state:
    st.session_state["last_modified_code"] = ""
if "processing" not in st.session_state:
    st.session_state["processing"] = False
if "stdout_output" not in st.session_state:
    st.session_state["stdout_output"] = ""
if "stderr_output" not in st.session_state:
    st.session_state["stderr_output"] = ""

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Use this app to modify your code with AI assistance.")

# Main UI
st.title("AI-Powered Code Modifier Chat")
st.subheader("Conversation History")
for message in st.session_state["conversation_history"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        explanation, code = message['content'].split("```python", 1)
        st.markdown(f"**AI Explanation:** {explanation.strip()}")
        st.code("```python" + code, language="python")

# Initial Code Input
st.subheader("Initial Code Input")
if not st.session_state["initial_code"]:
    initial_code = st.text_area("Enter your code:", height=150, placeholder="Paste your code here...")
    initial_request = st.text_input("Describe the initial modification you want:", placeholder="E.g., 'Add error handling'")

    if st.button("Send Initial Request") and not st.session_state["processing"]:
        if initial_code and initial_request:
            st.session_state["initial_code"] = initial_code
            st.session_state["processing"] = True  # Start processing to prevent duplicate submission

            with st.spinner("Processing request..."):
                # Retrieve memory for context and get AI response
                memory_context = get_memory(mem_client, user_id)
                ai_response = get_ai_response(client, initial_code, initial_request, memory_context)
                
                if ai_response:
                    modified_code = extract_code(ai_response)
                    # Update session state and memory
                    st.session_state["conversation_history"].append({"role": "user", "content": initial_request})
                    st.session_state["conversation_history"].append({"role": "assistant", "content": ai_response})
                    st.session_state["last_modified_code"] = modified_code
                    add_to_memory(mem_client, user_id, initial_request, ai_response)

            st.session_state["processing"] = False  # End processing

# Follow-up Requests
else:
    st.subheader("Follow-up Modification Request")
    followup_request = st.text_input("Describe the changes you want:", placeholder="E.g., 'Add type checks'")

    if st.button("Send Follow-up Request") and not st.session_state["processing"]:
        if followup_request:
            st.session_state["processing"] = True  # Start processing to prevent duplicate submission

            with st.spinner("Processing follow-up request..."):
                # Retrieve memory for context and get AI response
                memory_context = get_memory(mem_client, user_id)
                ai_response = get_ai_response(client, st.session_state["last_modified_code"], followup_request, memory_context)
                
                if ai_response:
                    modified_code = extract_code(ai_response)
                    # Update session state and memory
                    st.session_state["conversation_history"].append({"role": "user", "content": followup_request})
                    st.session_state["conversation_history"].append({"role": "assistant", "content": ai_response})
                    st.session_state["last_modified_code"] = modified_code
                    add_to_memory(mem_client, user_id, followup_request, ai_response)

            st.session_state["processing"] = False  # End processing

    # Button to execute the modified code
    if st.session_state["last_modified_code"]:
        if st.button("Run Modified Code"):
            stdout_output, stderr_output = execute_code(E2B_API_KEY, st.session_state["last_modified_code"])
            st.session_state["stdout_output"] = stdout_output or "No output generated"
            st.session_state["stderr_output"] = stderr_output or "No errors"

            st.subheader("Execution Results")
            st.text_area("Stdout", st.session_state["stdout_output"], height=100)
            st.text_area("Stderr", st.session_state["stderr_output"], height=100)

# Clear memory and reset conversation history
if st.sidebar.button("Clear Memory and Reset Chat"):
    mem_client.clear(user_id=user_id)
    st.session_state["conversation_history"] = []
    st.session_state["initial_code"] = ""
    st.session_state["last_modified_code"] = ""
    st.session_state["stdout_output"] = ""
    st.session_state["stderr_output"] = ""
    st.success("Memory and chat history cleared!")
