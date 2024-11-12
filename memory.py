from mem0 import MemoryClient

def initialize_memory_client(api_key):
    return MemoryClient(api_key=api_key)

def get_memory(mem_client, user_id):
    user_memories = mem_client.get_all(user_id=user_id)
    return "\n".join([memory['content'] for memory in user_memories])

def add_to_memory(mem_client, user_id, user_input, ai_response):
    memory_entry = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": ai_response}
    ]
    mem_client.add(memory_entry, user_id=user_id)