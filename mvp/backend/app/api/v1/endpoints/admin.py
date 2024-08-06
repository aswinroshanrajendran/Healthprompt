# # app/api/v1/endpoints/admin.py

# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from app.models.database import SessionLocal
# from app.models.user import User as DBUser, ActivityLog as DBActivityLog
# from app.models.schemas import UserCreate, UserResponse #, ActivityLogResponse
# from pydantic import BaseModel
# from datetime import datetime
# from app.models import user as models
# from typing import Optional

# router = APIRouter()

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/users/", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = DBUser(email=user.email, 
#                      password=user.password, 
#                      isadmin=user.isadmin,
#                      #
#                      firstname=user.firstname,
#                      lastname=user.lastname,
#                      date_of_birth=user.date_of_birth,
#                      gender=user.gender)
#                      #)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.get("/users/{user_id}", response_model=UserResponse)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.put("/users/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     db_user.email = user.email
#     db_user.password = user.password
#     db_user.isadmin = user.isadmin
#     #
#     db_user.firstname = user.firstname
#     db_user.lastname = user.lastname
#     db_user.date_of_birth = user.date_of_birth
#     db_user.gender = user.gender
#     #
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.delete("/users/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(db_user)
#     db.commit()
#     return {"message": "User deleted"}

# # @router.get("/activity_logs/", response_model=list[ActivityLogResponse])
# # def read_activity_logs(db: Session = Depends(get_db)):
# #     logs = db.query(DBActivityLog).all()
# #     return logs

# class LogActivityRequest(BaseModel):
#     user_id: int
#     activity_type: str
#     detail: str
#     source_language: Optional[str]

# class ActivityLogResponse(BaseModel):
#     action: str
#     details: str
#     timestamp: str
#     source_language: Optional[str]

#     class Config:
#         orm_mode = True

# @router.post("/log_user_activity/")
# def log_user_activity(request: LogActivityRequest, db: Session = Depends(get_db)):
#     db_log = DBActivityLog(user_id=request.user_id, 
#                            activity_type=request.activity_type, 
#                            detail=request.detail,
#                            source_language=request.source_language)
#     db.add(db_log)
#     db.commit()
#     db.refresh(db_log)
#     return {"message": "Activity logged successfully"}

# # @router.get("/activity_logs/", response_model=list[ActivityLogResponse])
# # def read_activity_logs(db: Session = Depends(get_db)):
# #     logs = db.query(models.ActivityLog).all()
# #     return [ActivityLogResponse(action=log.activity_type, details=log.detail, timestamp=log.timestamp.isoformat()) for log in logs]

# @router.get("/activity_logs/", response_model=list[ActivityLogResponse])
# def read_activity_logs(db: Session = Depends(get_db)):
#     logs = db.query(DBActivityLog).all()
#     return [ActivityLogResponse(action=log.activity_type, 
#                                 details=log.detail, 
#                                 source_language=log.source_language,
#                                 timestamp=log.timestamp.isoformat()) for log in logs]

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.user import User as DBUser, ActivityLog as DBActivityLog
from app.models.schemas import UserCreate, UserResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import hashlib


router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Received request: {user}")
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = DBUser(
        email=user.email, 
        password=user.password, 
        isadmin=user.isadmin,
        firstname=user.firstname,
        lastname=user.lastname,
        date_of_birth = user.date_of_birth,
        gender=user.gender
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"Created user: {db_user}")
    return db_user


# @router.post("/users/")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = create_user(db, user.email)
#     print(db_user)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
#     create_user(db, user.firstname, user.lastname, user.email, hashed_password, user.date_of_birth, user.gender)
#     return {"message": "User created successfully"}

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user and existing_user.id != user_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user.email = user.email
    db_user.password = user.password
    db_user.isadmin = user.isadmin
    db_user.firstname = user.firstname
    db_user.lastname = user.lastname
    db_user.date_of_birth = user.date_of_birth#datetime.strptime(user.date_of_birth, '%Y-%m-%d')  # Convert string to date
    db_user.gender = user.gender
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

class LogActivityRequest(BaseModel):
    user_id: int
    email: str
    activity_type: str
    detail: str
    source_language: Optional[str]
    recognized_text: str
    ner_result: str

class ActivityLogResponse(BaseModel):
    email: str
    action: str
    details: str
    timestamp: str
    source_language: Optional[str]
    recognized_text: str
    ner_result: str

    class Config:
        orm_mode = True

@router.post("/log_user_activity/")
def log_user_activity(request: LogActivityRequest, db: Session = Depends(get_db)):
    db_log = DBActivityLog(
        user_id=request.user_id, 
        email=request.email,
        activity_type=request.activity_type, 
        detail=request.detail,
        source_language=request.source_language,
        recognized_text= request.recognized_text,
        ner_result = request.ner_result
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return {"message": "Activity logged successfully"}

@router.get("/activity_logs/", response_model=list[ActivityLogResponse])
def read_activity_logs(db: Session = Depends(get_db)):
    logs = db.query(DBActivityLog).all()
    return [ActivityLogResponse(
        email=log.email,
        action=log.activity_type, 
        details=log.detail, 
        source_language=log.source_language or '',
        timestamp=log.timestamp.isoformat(),
        recognized_text=log.recognized_text or '',
        ner_result=log.ner_result or ''
    ) for log in logs]
