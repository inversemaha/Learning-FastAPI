from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING 

if TYPE_CHECKING:
    from schemas.category import CategoryResponse

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    """Used for POST request Validation."""
    pass

class ProductUpdate(ProductBase):
    """Used for PUT request Validation."""
    pass

class ProductResponse(ProductBase):
    """Used for sending back data to the client."""
    id: int
    category: Optional["CategoryResponse"] = None  # Proper forward reference

    class Config:
        orm_mode = True # Enables ORM to dict conversion for SQLAlchemy models

class MessageResponse(BaseModel):
    """Used for sending dict msg to the client."""
    message: str