def extract_code(response_content):
    # Find the start of the code block, either explicitly marked as Python or any code block
    code_start = response_content.find("```python")
    if code_start == -1:
        code_start = response_content.find("```")

    # Find the end of the code block
    code_end = response_content.rfind("```")

    # Extract and clean the code
    if code_start != -1 and code_end != -1:
        return response_content[code_start + len("```python"):code_end].strip()

    # If no code block is found, return an empty string or handle as needed
    return ""
