from fastapi import FastAPI
from core.log import logger
from settings import DATABASE_URL

app = FastAPI(title="SQL Agent Core")
text = "SQL Agent Core: Server running"
logger.info(text)

@app.get("/")
async def root():
    return {"message": text, "db_url": DATABASE_URL}
