from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib
import uvicorn
from app.crud.crud_user import get_user, create_user
from app.models.user import User
from app.models.database import Base, engine, SessionLocal
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    date_of_birth: str
    gender: str

class UserLogin(BaseModel):
    email: str
    password: str   

class UserResetPassword(BaseModel):
    email: str
    new_password: str

class LoginResponse(BaseModel):
    user_id: int
    email: str
    firstname: str
    lastname: str

@router.post("/signup/")
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.email)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    create_user(db, user.firstname, user.lastname, user.email, hashed_password, user.date_of_birth, user.gender)
    return {"message": "User created successfully"}

@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user(db, user.email)
    if not db_user or db_user.password != hashlib.sha256(user.password.encode()).hexdigest():
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return LoginResponse(
        user_id=db_user.id,
        email=db_user.email,
        firstname=db_user.firstname,
        lastname=db_user.lastname,
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/logout/")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"Invalidating token: {token}")
    return {"message": "Successfully logged out"}

@router.post("/reset-password/")
def reset_password(user: UserResetPassword, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email not found")
    hashed_password = hashlib.sha256(user.new_password.encode()).hexdigest()
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)
    return {"message": "Password reset successfully"}