def extract_code(response_content):
    code_start = response_content.find("```python")
    if code_start == -1:
        code_start = response_content.find("```")

    code_end = response_content.rfind("```")

    if code_start != -1 and code_end != -1 and code_end > code_start:
        return response_content[code_start + len("```python"):code_end].strip()

    return None
