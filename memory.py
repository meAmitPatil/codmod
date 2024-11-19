from mem0 import MemoryClient
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def initialize_memory_client(api_key):
    """
    Initialize the Mem0 Memory Client.
    """
    if not api_key:
        raise ValueError("Mem0 API key is missing.")
    return MemoryClient(api_key=api_key)

def get_memory(mem_client, user_id):
    """
    Fetch all memories for the given user ID.
    """
    try:
        # Fetch long-term memory for the user
        user_memories = mem_client.get_all(user_id=user_id, output_format="v1.1")
        logging.debug(f"Fetched memories for user {user_id}: {user_memories}")

        # Combine memory content for context
        memory_context = "\n".join([memory['content'] for memory in user_memories])
        return memory_context
    except Exception as e:
        logging.error(f"Error retrieving memory for user {user_id}: {e}")
        return ""

def add_to_memory(mem_client, user_id, user_input, ai_response):
    """
    Add user input and AI response to memory.
    """
    try:
        # Prepare memory messages
        messages = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": ai_response}
        ]

        # Add memory for the user
        mem_client.add(messages, user_id=user_id, output_format="v1.1")
        logging.debug(f"Added memory for user {user_id}: {messages}")
    except Exception as e:
        logging.error(f"Error adding memory for user {user_id}: {e}")

