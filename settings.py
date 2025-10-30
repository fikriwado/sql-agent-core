import os

if os.environ.get("ENVIRONMENT") != "os":
    from dotenv import load_dotenv
    load_dotenv()

# APPLICATION
APP_ENV = os.environ.get("APP_ENV")

# DATABASE
DATABASE_URL = os.environ.get("DATABASE_URL")

# LLM
LLM_BASE_URL = os.environ.get("LLM_BASE_URL")
LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME")
LLM_MAX_TOKENS = os.environ.get("LLM_MAX_TOKENS")
