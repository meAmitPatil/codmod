import os
from dotenv import load_dotenv

load_dotenv()

MEM0_API_KEY = os.getenv("MEM0_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

