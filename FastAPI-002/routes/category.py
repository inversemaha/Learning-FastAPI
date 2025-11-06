from fastapi import APIRouter, Depends, HTTPException
from config.database import session, engine
from schemas.category  import CategoryCreate, CategoryResponse
from models.category import Category as CategoryModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# 🟢 Get all categories
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    db_categories = db.query(CategoryModel).all()
    if not db_categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return db_categories

# 🟢 Create a new category
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# 🟢 Get category by ID
@router.get("/{id}", response_model=CategoryResponse)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
