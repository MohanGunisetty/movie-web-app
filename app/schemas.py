from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[str] = None

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Category Schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Movie Schemas
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: int

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class MovieResponse(MovieBase):
    id: int
    thumbnail_url: Optional[str] = None
    video_url: str
    uploaded_by: int
    created_at: datetime
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True
