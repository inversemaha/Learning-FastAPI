from fastapi import APIRouter, Depends, HTTPException
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from config.database import session, engine
import models.product as product_model
from sqlalchemy.orm import Session

router = APIRouter(prefix="/products", tags=["Products"])

product_model.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ProductResponse])
def get_all_product(db: Session = Depends(get_db)):
    db_product = db.query(product_model.Product).all()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/{id}", response_model=ProductResponse)
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    # Fetch product from DB
    db_product = db.query(product_model.Product).filter(product_model.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Fetch product data from request body
    db_product = product_model.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{id}", response_model=ProductResponse)
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    # Fetch product from DB
    db_product = db.query(product_model.Product).filter(product_model.Product.id == id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update fields from Pydantic model
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(product_model.Product).filter(product_model.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}