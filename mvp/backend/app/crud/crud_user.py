from app.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
from app.models.user import User
import app.models.database as database
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
import app.models.schemas as schemas
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(db:Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, firstname: str, lastname: str, email: str, password: str, date_of_birth: str, gender: str):
    db_user = User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password,
        date_of_birth=date_of_birth,
        gender=gender,
        isadmin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.firstname = user_update.firstname
        db_user.lastname = user_update.lastname
        db_user.date_of_birth = user_update.date_of_birth
        db_user.gender = user_update.gender
        db.commit()
        db.refresh(db_user)
    return db_user

def reset_password(db: Session, email: str, new_password: str):
    db_user = get_user(db, email)
    if db_user:
        db_user.password = new_password
        db.commit()
        db.refresh(db_user)
        return db_user
    return None