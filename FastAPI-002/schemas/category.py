from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    """Used for POST request Validation."""
    pass


class CategoryResponse(CategoryBase):
    """Public representation of a Category."""
    id: int

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    """Used for sending dict msg to the client."""
    message: str