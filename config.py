from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")