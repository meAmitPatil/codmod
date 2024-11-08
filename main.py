import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from mem0 import MemoryClient
import uuid
from e2b_code_interpreter import Sandbox

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mem_client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))
E2B_API_KEY = os.getenv("E2B_API_KEY")

# Set Streamlit page config
st.set_page_config(page_title="AI-Powered Code Modifier Chat", page_icon=":robot:")

# Generate or retrieve a unique user ID for the session
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(uuid.uuid4())
user_id = st.session_state['user_id']

# Initialize session state for conversation and code storage
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []
if "initial_code" not in st.session_state:
    st.session_state["initial_code"] = None
if "last_modified_code" not in st.session_state:
    st.session_state["last_modified_code"] = None

# Function to retrieve all memories of the current user
def get_memory():
    user_memories = mem_client.get_all(user_id=user_id)
    return "\n".join([memory['content'] for memory in user_memories])

# Function to add a new memory for the current user
def add_to_memory(user_input, ai_response):
    memory_entry = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": ai_response}
    ]
    mem_client.add(memory_entry, user_id=user_id)

# Function to execute code using E2B
def execute_code(code):
    with Sandbox(api_key=E2B_API_KEY) as code_interpreter:
        execution = code_interpreter.run_code(
            code,
            on_stdout=lambda stdout: st.text_area("Output", stdout, height=150),
            on_stderr=lambda stderr: st.text_area("Error", stderr, height=150)
        )
        
        if execution.error:
            st.error(f"Execution Error: {execution.error}")
        return execution

# Function to extract only the Python code from the AI response
def extract_code(response_content):
    # Remove markdown code block markers
    code_start = response_content.find("```python")
    code_end = response_content.rfind("```")
    
    # If code block markers are found, extract only the code within them
    if code_start != -1 and code_end != -1:
        return response_content[code_start + len("```python"):code_end].strip()
    
    # Otherwise, assume the whole content is code
    return response_content.strip()

# Title of the app
st.title("AI-Powered Code Modifier Chat")

# Display conversation history
for message in st.session_state["conversation_history"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        explanation, code = message['content'].split("```python", 1)
        st.markdown(f"**AI Explanation:** {explanation.strip()}")
        st.code("```python" + code, language="python")

# Initial Code Input
if st.session_state["initial_code"] is None:
    with st.form(key="initial_code_form", clear_on_submit=True):
        initial_code = st.text_area("Enter your code:", height=150, placeholder="Paste your code here...")
        initial_request = st.text_input("Describe the initial modification you want:", placeholder="E.g., 'Add error handling'")
        submit_button = st.form_submit_button(label="Send")

    if submit_button and initial_code and initial_request:
        st.session_state["initial_code"] = initial_code
        user_input = f"Code:\n{initial_code}\nRequest: {initial_request}"
        memory_context = get_memory()

        messages = [
            {"role": "system", "content": "You are an AI code modifier. Provide a detailed explanation followed by the complete Python code."},
            {"role": "user", "content": user_input}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.3
            )

            modified_response = response.choices[0].message.content
            modified_code = extract_code(modified_response)
            
            st.session_state["conversation_history"].append({"role": "user", "content": initial_request})
            st.session_state["conversation_history"].append({"role": "assistant", "content": modified_response})
            st.session_state["last_modified_code"] = modified_code
            add_to_memory(user_input, modified_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    with st.form(key="followup_form", clear_on_submit=True):
        followup_request = st.text_input("Describe the changes you want:", placeholder="E.g., 'Add type checks'")
        submit_followup = st.form_submit_button(label="Send")

    if submit_followup and followup_request:
        user_input = f"Request: {followup_request}"
        memory_context = get_memory()

        messages = [
            {"role": "system", "content": "You are an AI code modifier. Provide a detailed explanation followed by the complete Python code."},
            {"role": "user", "content": f"Here is the code:\n{st.session_state['last_modified_code']}\n\nPlease {followup_request}."}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.3
            )

            modified_response = response.choices[0].message.content
            modified_code = extract_code(modified_response)
            
            st.session_state["conversation_history"].append({"role": "user", "content": followup_request})
            st.session_state["conversation_history"].append({"role": "assistant", "content": modified_response})
            st.session_state["last_modified_code"] = modified_code
            add_to_memory(user_input, modified_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Provide a button to execute the modified code
    if st.session_state["last_modified_code"]:
        if st.button("Run Modified Code"):
            execution_output = execute_code(st.session_state["last_modified_code"])
            if execution_output:
                st.subheader("Execution Results")
                st.text_area("Stdout", execution_output.logs.stdout, height=100)
                st.text_area("Stderr", execution_output.logs.stderr, height=100)

# Button to clear memory and reset conversation history
if st.sidebar.button("Clear Memory and Reset Chat"):
    mem_client.clear(user_id=user_id)
    st.session_state["conversation_history"] = []
    st.session_state["initial_code"] = None
    st.session_state["last_modified_code"] = None
    st.success("Memory and chat history cleared!")
