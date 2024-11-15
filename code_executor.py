from e2b_code_interpreter import Sandbox
import logging

# Set up logging for debugging purposes
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_code(api_key, code):
    stdout_output = []
    stderr_output = []

    # Logging the code to be executed for debugging
    logging.debug("Code to execute:\n%s", code)

    # Initialize the sandbox environment with the provided API key
    with Sandbox(api_key=api_key) as code_interpreter:
        # Execute the code, capturing stdout and stderr in real-time
        execution = code_interpreter.run_code(
            code,
            on_stdout=lambda stdout: stdout_output.append(stdout.text if hasattr(stdout, 'text') else str(stdout)),
            on_stderr=lambda stderr: stderr_output.append(stderr.text if hasattr(stderr, 'text') else str(stderr))
        )

        # Check if there was an error during execution
        if execution.error:
            logging.error("Execution encountered an error: %s", execution.error)
            return "", f"Execution Error: {execution.error}"

    # Log the stdout and stderr outputs for debugging
    logging.debug("Stdout Output:\n%s", "\n".join(stdout_output))
    logging.debug("Stderr Output:\n%s", "\n".join(stderr_output))

    # Join stdout and stderr outputs into single strings and return them
    return "\n".join(stdout_output).strip(), "\n".join(stderr_output).strip()
