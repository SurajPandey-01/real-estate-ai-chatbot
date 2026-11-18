
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.retrieval import search_properties
from app.services.llm import generate_answer
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    context = search_properties(db, request.message)

    answer = generate_answer(request.message, context)

    sources = [
        {
            "name": item["name"],
            "source": item["source"],
            "url": item["url"],
        }
        for item in context
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
