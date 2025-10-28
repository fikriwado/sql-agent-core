from fastapi import FastAPI

app = FastAPI(title="OpenAI Integration")

@app.get("/")
async def root():
    return { "do": "something" }
