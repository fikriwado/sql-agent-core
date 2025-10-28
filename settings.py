import os
from core.log import logger

if os.environ.get("ENVIRONMENT") != "os":
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Load env from file")
else:
    logger.info("Load env from os")


DATABASE_URL = os.environ.get("DATABASE_URL")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL")
LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME")
LLM_MAX_TOKENS = os.environ.get("LLM_MAX_TOKENS")
