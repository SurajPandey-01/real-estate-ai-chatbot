
from fastapi import FastAPI

app = FastAPI(
    title="Real Estate AI Chatbot",
    description="AI assistant powered by DarGlobal and Wasalt data",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Real Estate AI Chatbot API is running!"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
