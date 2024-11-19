import requests
import json
from config import FIREWORKS_API_KEY
import logging

# Fireworks API call helper
def call_fireworks_api(prompt, model="accounts/fireworks/models/qwen2p5-coder-32b-instruct"):
    """
    Helper function to call the Fireworks API with a prompt and retrieve the response.
    """
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": model,
        "max_tokens": 4096,
        "temperature": 0.6,
        "messages": [{"role": "user", "content": prompt}]
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content'].strip()
        else:
            logging.error("No choices found in the API response.")
            return None
    else:
        logging.error(f"API call failed: {response.status_code} - {response.text}")
        return None

def get_qwen_response(code, request, memory_context=None):
    """
    Generate or refine Python code based on the provided request and memory context.
    """
    prompt = (
        "You are an advanced Python code assistant. Your goal is to modify and improve the following code based on the user's request. "
        "Ensure that the code is complete, executable, and follows Python best practices. "
        "Do not provide any explanations, only output the Python code in a code block starting with ```python."
    )
    if memory_context:
        prompt += f"\n\nMemory Context:\n{memory_context}"

    prompt += f"\n\nCode:\n```\n{code}\n```\n\nUser Request: {request}"
    return call_fireworks_api(prompt)

def get_qwen_feedback(generated_code):
    """
    Provides executable feedback on the given Python code.
    Instead of suggestions, it returns an improved/refined version of the code.
    """
    prompt = (
        "You are an AI feedback assistant. The following Python code needs improvement in terms of correctness, efficiency, and best practices. "
        "Generate an improved version of the code. Ensure the new code is executable and follows Python best practices. "
        "Do not include any explanations. Provide only the Python code in a code block starting with ```python."
        f"\n\nGenerated Code:\n```\n{generated_code}\n```"
    )
    return call_fireworks_api(prompt)
