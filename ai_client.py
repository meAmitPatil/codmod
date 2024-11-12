import openai

def initialize_openai_client(api_key):
    if api_key:
        openai.api_key = api_key
        return openai
    else:
        raise ValueError("OpenAI API key is missing.")

def get_ai_response(client, code, request, memory_context):
    messages = [
        {"role": "system", "content": "You are an AI code modifier. Provide a detailed explanation followed by the complete Python code."},
        {"role": "user", "content": f"Here is the code:\n{code}\n\nPlease {request}."}
    ]

    if memory_context:
        messages.insert(0, {"role": "system", "content": f"Use the following memory to understand user’s past requests and context:\n{memory_context}"})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.3
    )
    return response.choices[0].message.content
