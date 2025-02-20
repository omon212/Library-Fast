from enum import Enum
from pydantic import BaseModel
from fastapi import HTTPException


class ErrorCodes(str, Enum):
    USER_ALREADY_EXIST = "400_001"
    USER_UNAUTHORIZED = "400_002"
    INCORRECT_PASSWORD = "400_003"
    USER_NOT_FOUND = "400_004"
    USERNAME_ALREADY_EXIST = "400_005"
    TASK_NOT_FOUND = "400_006"
    BOOK_NOT_FOUND = "400_007"


class ErrorResponse(BaseModel):
    error_code: str
    message: str

class SuccessResponse(BaseModel):
    detail: str = "Success"

def exception(error_code: ErrorCodes, message: str) -> HTTPException:
    return HTTPException(
        status_code=400,
        detail=ErrorResponse(
            error_code=error_code.value,
            message=message,
        ).dict(),
    )

def success(code: int) -> HTTPException:
    return HTTPException(
        status_code=code,
        detail="Success",
    )
