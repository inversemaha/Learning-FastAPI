from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING

# TYPE_CHECKING prevents circular imports during runtime
if TYPE_CHECKING:
    from schemas.product import ProductResponse

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):    
    """Used for POST request Validation."""
    pass

class CategoryResponse(CategoryBase):
    id: int
    products: List["ProductResponse"] = [] # forward reference - matches model attribute name

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    """Used for sending dict msg to the client."""
    message: str