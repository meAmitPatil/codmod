from flask import Flask, request, render_template, jsonify, session
from config import MEM0_API_KEY, E2B_API_KEY
from memory import initialize_memory_client, get_memory, add_to_memory
from ai_client import get_qwen_response, get_qwen_feedback
from code_executor import execute_code
from utils import extract_code
import uuid
import logging
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key")  

log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
logging.basicConfig(level=log_level)

try:
    mem_client = initialize_memory_client(MEM0_API_KEY)
except Exception as e:
    logging.error(f"Failed to initialize Mem0 client: {e}")
    raise

@app.before_request
def set_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    global user_id
    user_id = session['user_id']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/modify_code', methods=['POST'])
def modify_code():
    data = request.json
    initial_code = data.get('initial_code', '').strip()
    modification_request = data.get('modification_request', '').strip()

    if not initial_code or not modification_request:
        return jsonify({'error': "Both initial code and modification request are required."}), 400

    try:
        memory_context = get_memory(mem_client, user_id)
        logging.debug(f"Memory context for user {user_id}: {memory_context}")

        ai_response = get_qwen_response(initial_code, modification_request, memory_context)
        if not ai_response:
            raise ValueError("Failed to generate code. AI response was empty.")

        # Extract generated code
        generated_code = extract_code(ai_response)
        if not generated_code:
            raise ValueError("Failed to extract generated code from AI response.")

        feedback_code = get_qwen_feedback(generated_code)
        if not feedback_code:
            logging.warning("Feedback generation failed. Proceeding with initial generated code.")
            feedback_code = generated_code

        metadata = {
            "operation": "code_modification",
            "context": "AI-generated code refinement",
            "language": "Python"
        }
        add_to_memory(mem_client, user_id, modification_request, {
            'generated_code': generated_code,
            'feedback_code': feedback_code
        }, metadata=metadata)

        return jsonify({'generated_code': feedback_code})

    except Exception as e:
        logging.error(f"Error in modify_code: {e}", exc_info=True)
        return jsonify({'error': f"Error in modify_code: {str(e)}"}), 500

@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.json
    code_to_run = data.get('code', '').strip()

    if not code_to_run:
        return jsonify({'error': "No code provided to execute."}), 400

    try:
        stdout_output, stderr_output = execute_code(E2B_API_KEY, code_to_run)

        logging.debug("Execution Results:")
        logging.debug("Stdout Output:\n%s", stdout_output)
        logging.debug("Stderr Output:\n%s", stderr_output)

        return jsonify({'stdout': stdout_output, 'stderr': stderr_output})

    except Exception as e:
        logging.error(f"Error during code execution: {str(e)}", exc_info=True)
        return jsonify({'error': f"Server Error: {str(e)}"}), 500

@app.route('/get_memory', methods=['GET'])
def retrieve_memory():
    try:
        memory_context = get_memory(mem_client, user_id)
        return jsonify({'memory_context': memory_context})
    except Exception as e:
        logging.error(f"Error retrieving memory: {str(e)}", exc_info=True)
        return jsonify({'error': f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
