from flask import Flask, request, render_template, jsonify
from config import MEM0_API_KEY, E2B_API_KEY
from memory import initialize_memory_client, get_memory, add_to_memory
from ai_client import get_qwen_response, get_qwen_feedback
from code_executor import execute_code
from utils import extract_code
import uuid
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize memory client
mem_client = initialize_memory_client(MEM0_API_KEY)
user_id = str(uuid.uuid4())  # Unique ID for each user session

# Variable to store final code for execution
final_code = ""

@app.route('/')
def home():
    return render_template('index.html')

# Endpoint for AI modification requests
@app.route('/modify_code', methods=['POST'])
def modify_code():
    global final_code
    data = request.json
    initial_code = data.get('initial_code', '')
    modification_request = data.get('modification_request', '')

    try:
        # Fetch memory context for the user
        memory_context = get_memory(mem_client, user_id)
        logging.debug(f"Memory context for user {user_id}: {memory_context}")

        # Step 1: Generate code with AI
        ai_response = get_qwen_response(initial_code, modification_request, memory_context)
        if not ai_response:
            raise ValueError("Failed to generate code. AI response was empty.")

        # Extract the generated code
        generated_code = extract_code(ai_response)
        if not generated_code:
            raise ValueError("Failed to extract generated code from AI response.")

        # Step 2: Generate feedback for the generated code
        feedback_code = get_qwen_feedback(generated_code)
        if not feedback_code:
            raise ValueError("Failed to generate feedback.")

        # Step 3: Generate final code after feedback refinement
        final_response = get_qwen_response(feedback_code, modification_request)
        final_code = extract_code(final_response)
        if not final_code:
            raise ValueError("Failed to extract final code from feedback refinement.")

        # Save the interaction to memory
        add_to_memory(mem_client, user_id, modification_request, final_code)

        # Return only the final code to the frontend
        return jsonify({'generated_code': final_code})

    except Exception as e:
        logging.error(f"Error in modify_code: {e}")
        return jsonify({'error': str(e)}), 500


# Endpoint for code execution
@app.route('/run_code', methods=['POST'])
def run_code():
    global final_code

    try:
        # Execute the final code
        stdout_output, stderr_output = execute_code(E2B_API_KEY, final_code)

        # Log the outputs for debugging
        logging.debug("Execution Results:")
        logging.debug("Stdout Output:\n%s", stdout_output)
        logging.debug("Stderr Output:\n%s", stderr_output)

        # Return the execution results
        return jsonify({'stdout': stdout_output, 'stderr': stderr_output})
    except Exception as e:
        logging.error(f"Error during code execution: {str(e)}")
        return jsonify({'error': f"Server Error: {str(e)}"}), 500

# Endpoint to test memory retrieval (for debugging purposes)
@app.route('/get_memory', methods=['GET'])
def retrieve_memory():
    try:
        memory_context = get_memory(mem_client, user_id)
        return jsonify({'memory_context': memory_context})
    except Exception as e:
        logging.error(f"Error retrieving memory: {str(e)}")
        return jsonify({'error': f"Server Error: {str(e)}"}), 500

# Endpoint to test adding memory (for debugging purposes)
@app.route('/add_memory', methods=['POST'])
def add_memory():
    data = request.json
    user_input = data.get('user_input', '')
    ai_response = data.get('ai_response', '')

    try:
        add_to_memory(mem_client, user_id, user_input, ai_response)
        return jsonify({'message': "Memory added successfully."})
    except Exception as e:
        logging.error(f"Error adding memory: {str(e)}")
        return jsonify({'error': f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
