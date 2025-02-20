from math import ceil
from typing import TypeVar, List, Any, Dict, Generic

from pydantic import BaseModel


T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    current_page: int
    limit: int
    pages: int
    data_count: int
    data: List[T]

    class Config:
        from_attributes = True


class Pagination:
    def __init__(self, query, page: int = 1, limit: int = 10):
        self.query = query
        self.page = page
        self.limit = limit
        self.total_count = query.count()
        self.total_pages = ceil(self.total_count / limit)

    def get_paginated_response(self) -> Dict[str, Any]:

        offset = (self.page - 1) * self.limit
        items = self.query.offset(offset).limit(self.limit).all()

        return {
            "current_page": self.page,
            "limit": self.limit,
            "pages": self.total_pages,
            "data_count": self.total_count,
            "data": items,
        }
