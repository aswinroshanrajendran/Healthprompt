from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.schemas import FeedbackRequest, FeedbackResponse
from app.models.models import Feedback
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback/", response_model=FeedbackResponse)
def create_feedback(feedback_request: FeedbackRequest, db: Session = Depends(get_db)):
    db_feedback = Feedback(
        original_text=feedback_request.original_text,
        feedback=feedback_request.serialize_feedback()  # Pass the list directly
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.get("/feedback/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Deserialize feedback for the response
    db_feedback.feedback = json.loads(db_feedback.feedback)
    return db_feedback
