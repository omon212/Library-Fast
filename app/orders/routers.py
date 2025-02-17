from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.databace import get_db
from app.orders.models import Order
from app.orders.schemas import OrderCreate, OrderUpdate, OrderResponse
from typing import List

orders = APIRouter(prefix="/orders", tags=["orders"])


@orders.post("/create/", response_model=OrderResponse, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(**order_data.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@orders.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order_data.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


@orders.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@orders.get("/user/{user_id}", response_model=List[OrderResponse])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == user_id).all()


@orders.get("/{order_id}", response_model=OrderResponse)
def get_user_order(order_id: int, user_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
