from dotenv import load_dotenv
import os

load_dotenv()

class Setting:
    DATABASE_URL = os.getenv("DATABASE_URL")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
    LLM_MAX_TOKENS = os.getenv("LLM_MAX_TOKENS")

setting = Setting()
