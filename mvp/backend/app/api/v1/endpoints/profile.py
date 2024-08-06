from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.crud_user import get_user_by_id, update_user
from app.models.schemas import UserUpdate
from app.models.database import Base, engine, SessionLocal

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/profile/{user_id}", response_model=UserUpdate)
def read_user_profile(user_id: int, db: Session = Depends(get_db)):
    print("i a ere")
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/profile/{user_id}", response_model=UserUpdate)
def update_user_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
