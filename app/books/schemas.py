from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    count: int
    daily_price: float
    is_available: Optional[bool] = True

class BookResponse(BookCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: int
    comment: Optional[str] = None

class ReviewResponse(ReviewCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
