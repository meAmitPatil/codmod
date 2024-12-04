from e2b_code_interpreter import Sandbox
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_code(api_key, code):
    stdout_output = []
    stderr_output = []

    logging.debug("Code to execute:\n%s", code)

    with Sandbox(api_key=api_key) as code_interpreter:
        execution = code_interpreter.run_code(
            code,
            on_stdout=lambda stdout: stdout_output.append(stdout.text if hasattr(stdout, 'text') else str(stdout)),
            on_stderr=lambda stderr: stderr_output.append(stderr.text if hasattr(stderr, 'text') else str(stderr))
        )
        
        if execution.error:
            logging.error("Execution encountered an error: %s", execution.error)
            return "", f"Execution Error: {execution.error}"

    logging.debug("Stdout Output:\n%s", "\n".join(stdout_output))
    logging.debug("Stderr Output:\n%s", "\n".join(stderr_output))

    return "\n".join(stdout_output).strip(), "\n".join(stderr_output).strip()
