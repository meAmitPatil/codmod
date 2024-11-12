from e2b_code_interpreter import Sandbox

def execute_code(api_key, code):
    stdout_output = []
    stderr_output = []

    with Sandbox(api_key=api_key) as code_interpreter:
        execution = code_interpreter.run_code(
            code,
            on_stdout=lambda stdout: stdout_output.append(getattr(stdout, 'text', str(stdout))),
            on_stderr=lambda stderr: stderr_output.append(getattr(stderr, 'text', str(stderr)))
        )
        
        if execution.error:
            raise RuntimeError(f"Execution Error: {execution.error}")
        
    return "\n".join(stdout_output), "\n".join(stderr_output)