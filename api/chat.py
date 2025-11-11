import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_db
from core.consolidation import consolidation_engine

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: str | None = None
    user_id: str
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    assistant_message: str
    interaction_id: str

@router.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Simulates a chat interaction and triggers the consolidation engine.
    """
    # If no conversation_id is provided, create a new one
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # In a real app, this is where the LLM would generate a response.
    # For now, we'll just mock a response.
    assistant_response = f"This is a mocked response to: '{request.message}'"

    try:
        # This is the core logic: trigger consolidation
        interaction = consolidation_engine.consolidate_interaction(
            db=db,
            conversation_id=conversation_id,
            user_id=request.user_id,
            user_message=request.message,
            assistant_message=assistant_response,
        )
        
        return ChatResponse(
            conversation_id=conversation_id,
            assistant_message=assistant_response,
            interaction_id=str(interaction.id)
        )
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")