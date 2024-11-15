from flask import Flask, request, render_template, jsonify
from config import MEM0_API_KEY, E2B_API_KEY
from memory import initialize_memory_client, get_memory, add_to_memory
from ai_client import get_qwen_response
from code_executor import execute_code
from utils import extract_code
import uuid
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize memory client
mem_client = initialize_memory_client(MEM0_API_KEY)
user_id = str(uuid.uuid4())

@app.route('/')
def home():
    return render_template('index.html')

# Endpoint for AI modification requests
@app.route('/modify_code', methods=['POST'])
def modify_code():
    data = request.json
    initial_code = data.get('initial_code', '')
    modification_request = data.get('modification_request', '')

    try:
        memory_context = get_memory(mem_client, user_id)
        ai_response = get_qwen_response(initial_code, modification_request, memory_context)

        # Log the AI response for debugging
        logging.debug(f"AI Response: {ai_response}")

        # Check if the response is an error message
        if ai_response.startswith("Error:"):
            return jsonify({'error': ai_response}), 500
        
        # Extract the modified code from the AI response
        modified_code = extract_code(ai_response)
        if not modified_code:
            return jsonify({'error': "No modified code returned."}), 400
        
        # Save the interaction to memory
        add_to_memory(mem_client, user_id, modification_request, ai_response)

        # Return the AI response and the extracted modified code
        return jsonify({'ai_response': ai_response, 'modified_code': modified_code})

    except Exception as e:
        logging.error(f"Error in modify_code: {str(e)}")  # Log the error
        return jsonify({'error': f"Server Error: {str(e)}"}), 500

# Endpoint for code execution
@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.json
    code_to_run = data.get('code', '')

    try:
        stdout_output, stderr_output = execute_code(E2B_API_KEY, code_to_run)

        # Log the outputs for debugging
        logging.debug("Execution Results:")
        logging.debug("Stdout Output:\n%s", stdout_output)
        logging.debug("Stderr Output:\n%s", stderr_output)

        return jsonify({'stdout': stdout_output, 'stderr': stderr_output})
    except Exception as e:
        logging.error(f"Error during code execution: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
