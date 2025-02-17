from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderBase(BaseModel):
    user_id: int
    book_id: int
    start_date: datetime
    end_date: datetime
    status: str = "WAITING"


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    returned_at: Optional[datetime] = None
    status: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True
