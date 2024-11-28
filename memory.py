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
    try:
        client = MemoryClient(api_key=api_key)
        logging.info("Mem0 Memory Client initialized successfully.")
        return client
    except Exception as e:
        logging.error(f"Error initializing Mem0 Memory Client: {e}")
        raise

def get_memory(mem_client, user_id):
    """
    Fetch all memories for the given user ID.
    """
    try:
        # Fetch long-term memory for the user
        user_memories = mem_client.get_all(user_id=user_id, output_format="v1.1", page=1, page_size=100)
        logging.debug(f"Fetched memories for user {user_id}: {user_memories}")

        # Correctly extract nested `results`
        memory_results = user_memories.get("results", [])
        if isinstance(memory_results, dict) and "results" in memory_results:
            memory_results = memory_results["results"]

        # Combine memory content for context
        memory_context = "\n".join([memory['content'] for memory in memory_results])
        return memory_context
    except Exception as e:
        logging.error(f"Error retrieving memory for user {user_id}: {e}")
        return ""

def add_to_memory(mem_client, user_id, user_input, ai_response, metadata=None):
    """
    Add user input and AI response to memory with optional metadata.
    """
    try:
        # Prepare memory messages
        messages = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": ai_response if isinstance(ai_response, str) else str(ai_response)}
        ]

        # Log the request data for debugging
        logging.debug(f"Adding memory for user {user_id} with messages: {messages} and metadata: {metadata}")

        # Add memory with optional metadata
        response = mem_client.add(
            messages=messages,
            user_id=user_id,
            output_format="v1.1",
            metadata=metadata  # Metadata is optional
        )
        logging.debug(f"Memory added successfully. Response: {response}")
    except Exception as e:
        logging.error(f"Error adding memory for user {user_id}: {e}")
        raise

