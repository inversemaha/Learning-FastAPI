from pydantic import BaseModel
from typing import List, Optional
from schemas.product import Product


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(BaseModel):    
    """Used for POST request Validation."""
    pass

class Category(CategoryBase):
    id: int
    product: List["Product"] = [] # forward referance

    class Config:
        orm_mode = True