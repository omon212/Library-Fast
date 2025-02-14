from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.databace import get_db
from app.users.models import User
from app.users.auth import create_access_token, oauth2_scheme, verify_token
from fastapi.responses import Response
from app.users.schemas import RegisterSchema, LoginSchema
from app.users.auth import blacklisted_tokens, revoke_access_token

user = APIRouter(prefix="/user", tags=["Auth"])


@user.post("/register", status_code=200)
async def user_register(user: RegisterSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User Already Exists")

    new_user = User(username=user.username, password=user.password, role=user.role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User Created"}


@user.post("/login", status_code=200)
async def user_login(user: LoginSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User Not Found")

    access_token = create_access_token(
        data={"id": existing_user.id, "username": existing_user.username, "role": existing_user.role})

    return {"message": "User Login Successfully", "access_token": access_token, "token_type": "bearer"}


@user.get("/me", status_code=200)
def read_users_me(token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return verify_token(token)


@user.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username, "role": user.role} for user in users]


@user.post("/logout", status_code=200)
async def logout(response: Response, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Not authenticated")

    revoke_access_token(token)
    response.delete_cookie("access_token")
    return {"message": "User Logged Out Successfully"}
