from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: str
    isadmin: bool

class UserCreate(UserBase):
    password: str
    firstname: str
    lastname: str
    date_of_birth: str
    gender: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    firstname: str
    lastname: str
    date_of_birth: datetime
    gender: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    firstname: str
    lastname: str
    date_of_birth: datetime
    gender: str
    email: str


class FeedbackItem(BaseModel):
    comment: str

class FeedbackRequest(BaseModel):
    original_text: str
    feedback: List[FeedbackItem]

    def serialize_feedback(self) -> List[dict]:
        return [item.dict() for item in self.feedback]

class FeedbackResponse(BaseModel):
    id: int
    original_text: str
    feedback: List[FeedbackItem]  # Assuming feedback is deserialized here

    class Config:
        orm_mode = True

# class ActivityLogCreate(BaseModel):
#     user_id: int
#     action: str
#     details: Optional[str]

# class ActivityLogResponse(BaseModel):
#     id: int
#     user_id: int
#     action: str
#     details: Optional[str]
#     timestamp: str

#     class Config:
#         orm_mode = True
