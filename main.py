from fastapi import FastAPI
from core.log import logger

app = FastAPI(title="OpenAI Integration")

text = "OpenAI Integration: Server running"
logger.info(text)

@app.get("/")
async def root():
    return text
