from fastapi import APIRouter, Request, Query, HTTPException
from pydantic import BaseModel

from app.utils.validation import validate_guest_id, validate_question

qa_router = APIRouter(prefix="/qa", tags=["qa"])

class QuestionRequest(BaseModel):
    question: str

@qa_router.post("/ask")
async def ask(
    request: Request,
    req: QuestionRequest,
    guest_id: str = Query(..., description="The unique guest ID")
):
    validate_guest_id(guest_id)
    validate_question(req.question)

    app = request.app
    return await app.qa_service.ask(req.question, guest_id)