from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.databace import get_db
from app.books.models import Book, Review
from app.books.schemas import BookCreate, BookResponse, ReviewCreate, ReviewResponse
from typing import List
from app.users.auth import oauth2_scheme
from app.users.auth import blacklisted_tokens, verify_token
from app.base.paginations import Pagination, PaginatedResponse
from app.base.exceptions import exception, ErrorCodes, ErrorResponse

books = APIRouter(prefix="/books", tags=["Books"])


@books.get(
    "/",
    response_model=PaginatedResponse[BookResponse],
    name="get_books"
)
def get_books(page: int, limit: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise exception(
            ErrorCodes.USER_UNAUTHORIZED,
            "User not authorized",
        )

    user = verify_token(token)
    books = db.query(Book)
    return Pagination(books, page, limit).get_paginated_response()


@books.post(
    "/create/",
    response_model=BookResponse,
    name="create_book"
)
def create_book(book: BookCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise exception(
            ErrorCodes.USER_UNAUTHORIZED,
            "User not authorized",
        )

    user = verify_token(token)
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@books.get(
    "/{pk}/",
    response_model=BookResponse,
    name="get_book",
    responses={
        400: {
            "model": ErrorResponse
        }
    }
)
def get_book(pk: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise exception(
            ErrorCodes.USER_UNAUTHORIZED,
            "User not authorized",
        )

    user = verify_token(token)
    book = db.query(Book).filter(Book.id == pk).first()
    if not book:
        raise exception(
            ErrorCodes.BOOK_NOT_FOUND,
            "Book not found",
        )
    return book


@books.put(
    "/{pk}/update/",
    response_model=BookResponse,
    name="update_book"
)
def update_book(pk: int, book_data: BookCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = verify_token(token)
    book = db.query(Book).filter(Book.id == pk).first()
    if not book:
        raise exception(
            ErrorCodes.BOOK_NOT_FOUND,
            "Book not found"
        )
    for key, value in book_data.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


@books.delete(
    "/{pk}/delete/",
    name="delete_book"
)
def delete_book(pk: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise exception(
            ErrorCodes.USER_UNAUTHORIZED,
            "User not authorized",
        )

    user = verify_token(token)
    book = db.query(Book).filter(Book.id == pk).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


@books.get(
    "/{pk}/reviews/",
    response_model=List[ReviewResponse],
    name="get_book_reviews"
)
def get_book_reviews(pk: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise exception(
            ErrorCodes.USER_UNAUTHORIZED,
            "User not authorized",
        )

    user = verify_token(token)
    reviews = db.query(Review).filter(Review.book_id == pk).all()
    return reviews


@books.post(
    "/reviews/",
    response_model=ReviewResponse,
    name="write_review"
)
def write_review(review: ReviewCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise exception(
            ErrorCodes.USER_UNAUTHORIZED,
            "User not authorized",
        )

    user = verify_token(token)
    new_review = Review(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
