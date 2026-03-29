from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    face_image: str  # base64 encoded image
    nickname: Optional[str] = None
    exp: Optional[int] = None
    email: Optional[str] = None


class UserUpdate(BaseModel):
    password: Optional[str] = None
    face_image: Optional[str] = None  # base64 encoded image
    nickname: Optional[str] = None
    exp: Optional[int] = None
    email: Optional[str] = None


class UserOut(UserBase):
    id: int
    password: Optional[str] = None
    nickname: Optional[str] = None
    exp: Optional[int] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    id: int
    password: str
    face_image: str  # base64 encoded image
    nickname: Optional[str] = None
    exp: Optional[int] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class ControlCommand(BaseModel):
    command: str


class Record(BaseModel):
    username: str
    timestamp: str  # ISO 8601 formatted string (e.g., "2023-05-17T14:30:00")

    class Config:
        orm_mode = True


class DetectionResult(BaseModel):
    annotated_image: str  # base64 encoded image
    username: Optional[str] = None
