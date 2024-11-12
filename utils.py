def extract_code(response_content):
    code_start = response_content.find("```python")
    code_end = response_content.rfind("```")
    if code_start != -1 and code_end != -1:
        return response_content[code_start + len("```python"):code_end].strip()
    return response_content.strip()