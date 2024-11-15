import requests
import json
from config import FIREWORKS_API_KEY
import logging

def get_qwen_response(code, request, memory_context=None):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    
    # Define the prompt with clear instructions for output formatting
    system_prompt = (
        "You are an AI code assistant. "
        "First, provide a brief explanation (1-3 sentences) about the modification. "
        "Then output the modified Python code ONLY within a code block, "
        "starting with ```python and ending with ```. "
        "Do not include additional text outside of the code block at the end. "
        "Ensure the code is complete and can be executed independently."
    )
    if memory_context:
        system_prompt += f"\nUse the following memory to understand user’s past requests and context:\n{memory_context}"

    # Construct the payload
    payload = {
        "model": "accounts/fireworks/models/qwen2p5-coder-32b-instruct",
        "max_tokens": 4096,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the code:\n{code}\n\nPlease {request}."}
        ]
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}"
    }
    
    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Handle the response
    if response.status_code == 200:
        result = response.json()
        logging.debug(f"API Response JSON: {result}")  # Log the full response

        # Check if 'choices' and 'message' are in the response
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            return content
        else:
            return "Error: No response received from Qwen."
    else:
        return f"Error: {response.status_code} - {response.text}"
