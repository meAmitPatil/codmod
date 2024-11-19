def extract_code(response_content):
    """
    Extracts the Python code block from the response content.
    Handles both ` ```python ` and ` ``` ` blocks.
    """
    # Check for "```python" code blocks
    code_start = response_content.find("```python")
    if code_start == -1:
        # If not found, check for generic "```" code blocks
        code_start = response_content.find("```")

    code_end = response_content.rfind("```")

    # Extract and clean the code
    if code_start != -1 and code_end != -1 and code_end > code_start:
        # Extract the code and strip whitespace or unwanted content
        return response_content[code_start + len("```python"):code_end].strip()

    # Return None if no valid code block is found
    return None
