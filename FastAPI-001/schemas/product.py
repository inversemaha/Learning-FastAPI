from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    """Used for POST request Validation."""
    pass

class ProductUpdate(ProductBase):
    """Used for PUT request Validation."""
    pass

class ProductResponse(ProductBase):
    """Used for sending back data to the client."""
    id: int

    class Config:
        orm_mode = True # Enables ORM to dict conversion for SQLAlchemy models

class MessageResponse(BaseModel):
    """Used for sending dict msg to the client."""
    message: str