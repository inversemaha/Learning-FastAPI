
# 📚 FastAPI Knowledge Base - Complete Beginner's Guide

## 🎯 Purpose
This is your comprehensive reference guide for understanding all the libraries, concepts, and tools used in FastAPI development. Each section explains **what it is**, **how it works**, and **when to use it**.

---

## 🛣️ FastAPI Core Components

### 1. **APIRouter**
```python
from fastapi import APIRouter
router = APIRouter(prefix="/products", tags=["Products"])
```

**What it is:**
- A way to organize your API endpoints into separate modules
- Like creating separate "sections" for your API

**How it works:**
- Groups related endpoints together
- Adds common prefixes and tags
- Keeps code organized and modular

**When to use:**
- ✅ When you have multiple endpoints for the same resource (products, users, etc.)
- ✅ When you want to organize large applications
- ✅ When you want to add common middleware to a group of routes

**Example:**
```python
# routes/product.py
router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")           # Creates: GET /products/
@router.post("/")          # Creates: POST /products/
@router.get("/{id}")       # Creates: GET /products/{id}

# main.py
app.include_router(router)  # Registers all routes
```

**Real-world analogy:** Like organizing books in a library - all Python books go in the Python section, all history books in the history section.

---

### 2. **Depends**
```python
from fastapi import Depends
def get_categories(db: Session = Depends(get_db)):
```

**What it is:**
- Dependency Injection system
- A way to "inject" common functionality into your endpoints

**How it works:**
- FastAPI automatically calls the dependency function
- Passes the result to your endpoint function
- Handles cleanup automatically

**When to use:**
- ✅ Database connections (`get_db`)
- ✅ Authentication (`get_current_user`)
- ✅ Configuration settings
- ✅ Anything you need in multiple endpoints

**Example:**
```python
# Dependency function
def get_db():
    db = session()
    try:
        yield db    # Provides database session
    finally:
        db.close()  # Cleanup happens automatically

# Using dependency
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
```

**Real-world analogy:** Like a waiter in a restaurant - you don't have to go to the kitchen yourself, the waiter brings you what you need.

---

### 3. **HTTPException**
```python
from fastapi import HTTPException
raise HTTPException(status_code=404, detail="Product not found")
```

**What it is:**
- A way to return HTTP error responses
- FastAPI's standard way to handle errors

**How it works:**
- Stops execution immediately
- Returns proper HTTP status codes
- Sends error message to client

**When to use:**
- ✅ When data is not found (404)
- ✅ When user is not authorized (401, 403)
- ✅ When validation fails (422)
- ✅ When server errors occur (500)

**Common Status Codes:**
```python
# Not Found
raise HTTPException(status_code=404, detail="Product not found")

# Unauthorized  
raise HTTPException(status_code=401, detail="Invalid credentials")

# Forbidden
raise HTTPException(status_code=403, detail="Not enough permissions")

# Bad Request
raise HTTPException(status_code=400, detail="Invalid input data")

# Unprocessable Entity
raise HTTPException(status_code=422, detail="Validation error")
```

**Real-world analogy:** Like a security guard - stops you and explains why you can't proceed.

---

## 🐍 Python Type Hints

### 4. **List**
```python
from typing import List
products: List[ProductResponse] = []
```

**What it is:**
- Type hint for lists/arrays
- Tells Python (and your IDE) what type of items are in the list

**How it works:**
- `List[int]` = list of integers
- `List[str]` = list of strings
- `List[ProductResponse]` = list of Product objects

**When to use:**
- ✅ Function parameters that expect lists
- ✅ Function return values that return lists
- ✅ Class attributes that store lists

**Example:**
```python
# Without type hints (unclear)
def get_products():
    return products

# With type hints (clear)
def get_products() -> List[ProductResponse]:
    return products

# IDE knows it's a list of ProductResponse objects
results = get_products()
results[0].name  # IDE can autocomplete!
```

---

### 5. **Optional**
```python
from typing import Optional
category_id: Optional[int] = None
```

**What it is:**
- Type hint meaning "this can be the specified type OR None"
- Equivalent to `Union[int, None]`

**How it works:**
- `Optional[int]` = can be integer or None
- `Optional[str]` = can be string or None
- Makes it clear that None is an acceptable value

**When to use:**
- ✅ Database fields that can be NULL
- ✅ Function parameters with default values
- ✅ Optional configuration settings

**Example:**
```python
class Product(BaseModel):
    name: str                    # Required
    category_id: Optional[int] = None  # Optional

# Valid data
product1 = Product(name="Laptop", category_id=1)    # ✅
product2 = Product(name="Mouse", category_id=None)   # ✅
product3 = Product(name="Keyboard")                  # ✅ (category_id defaults to None)
```

---

### 6. **TYPE_CHECKING**
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from schemas.product import ProductResponse
```

**What it is:**
- A flag that's `True` during type checking, `False` during runtime
- Prevents circular import errors

**How it works:**
- Code inside `if TYPE_CHECKING:` only runs when type checker analyzes code
- Doesn't run when your program actually executes
- Allows forward references without circular imports

**When to use:**
- ✅ When you have circular imports between schemas
- ✅ When you need forward references
- ✅ When type checkers need imports that would cause runtime errors

**Example:**
```python
# schemas/category.py
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from schemas.product import ProductResponse  # Only for type checking

class CategoryResponse(BaseModel):
    id: int
    name: str
    products: List["ProductResponse"] = []  # Forward reference in quotes
```

**Real-world analogy:** Like a blueprint vs. actual construction - you can reference other blueprints in the planning phase, but during construction you work on one building at a time.

---

## 📋 Pydantic (Data Validation)

### 7. **BaseModel**
```python
from pydantic import BaseModel
class ProductCreate(BaseModel):
    name: str
    price: float
```

**What it is:**
- Base class for all Pydantic models
- Provides automatic data validation and serialization

**How it works:**
- Automatically validates input data types
- Converts data to/from JSON
- Provides helpful error messages
- Generates JSON schemas

**When to use:**
- ✅ API request/response models
- ✅ Configuration classes
- ✅ Data transfer objects
- ✅ Anywhere you need validated data structures

**Features:**
```python
class Product(BaseModel):
    name: str
    price: float
    quantity: int = 0  # Default value

# Automatic validation
product = Product(name="Laptop", price="999.99")  # String gets converted to float
print(product.price)  # 999.99 (float)

# JSON serialization
print(product.json())  # {"name": "Laptop", "price": 999.99, "quantity": 0}

# Dictionary conversion
print(product.dict())  # {"name": "Laptop", "price": 999.99, "quantity": 0}
```

**Validation Example:**
```python
# This will raise validation error
try:
    Product(name="Laptop", price="invalid")  # ❌ Can't convert "invalid" to float
except ValidationError as e:
    print(e.errors())  # Shows exactly what's wrong
```

---

### 8. **model_rebuild() / rebuild_models**
```python
CategoryResponse.model_rebuild()
ProductResponse.model_rebuild()
```

**What it is:**
- A method that resolves forward references in Pydantic models
- Fixes circular import issues

**How it works:**
- Re-analyzes the model after all classes are defined
- Resolves quoted type hints like `"ProductResponse"`
- Must be called after all related models are imported

**When to use:**
- ✅ After defining models with forward references
- ✅ When you get `PydanticUserError: not fully defined`
- ✅ In your main.py after importing all schemas

**Example:**
```python
# schemas/category.py
class CategoryResponse(BaseModel):
    products: List["ProductResponse"] = []  # Forward reference

# main.py
from schemas.category import CategoryResponse
from schemas.product import ProductResponse

# Now resolve the forward references
CategoryResponse.model_rebuild()  # Now "ProductResponse" gets resolved
ProductResponse.model_rebuild()
```

---

## 🗄️ SQLAlchemy (Database ORM)

### 9. **Session**
```python
from sqlalchemy.orm import Session
def get_products(db: Session = Depends(get_db)):
```

**What it is:**
- Database connection and transaction manager
- Your interface to the database

**How it works:**
- Manages database connections
- Handles transactions (commit/rollback)
- Tracks changes to objects
- Executes queries

**When to use:**
- ✅ Every database operation (query, insert, update, delete)
- ✅ As dependency in FastAPI routes
- ✅ Managing database transactions

**Common Operations:**
```python
def crud_operations(db: Session):
    # Query
    products = db.query(Product).all()
    product = db.query(Product).filter(Product.id == 1).first()
    
    # Create
    new_product = Product(name="New Item", price=99.99)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # Get updated data from DB
    
    # Update
    product.price = 199.99
    db.commit()
    
    # Delete
    db.delete(product)
    db.commit()
```

**Session Lifecycle:**
```python
def get_db():
    db = session()  # Create session
    try:
        yield db    # Use session
    finally:
        db.close()  # Always close session
```

---

## 🔄 Database Migrations

### 10. **Alembic**
```python
# Command line tool
alembic init alembic
alembic revision --autogenerate -m "Add categories table"
alembic upgrade head
```

**What it is:**
- Database migration tool for SQLAlchemy
- Tracks and manages database schema changes

**How it works:**
- Compares your models to current database schema
- Generates migration scripts automatically
- Applies changes in order
- Tracks what's been applied

**When to use:**
- ✅ When you change model structure (add/remove columns)
- ✅ When you add new tables
- ✅ When you need to modify existing data
- ✅ In production environments (safer than dropping tables)

**Workflow:**
```bash
# 1. Initialize (once per project)
alembic init alembic

# 2. Configure alembic.ini and env.py
# Edit database URL and import your models

# 3. Generate migration
alembic revision --autogenerate -m "Add category_id to products"

# 4. Review generated migration file
# Check if it does what you expect

# 5. Apply migration
alembic upgrade head

# 6. Check migration status
alembic current
alembic history
```

**Migration File Example:**
```python
def upgrade():
    op.add_column('product', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_product_category', 'product', 'category', ['category_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_product_category', 'product', type_='foreignkey')
    op.drop_column('product', 'category_id')
```

---

## 📦 Additional Important Libraries

### 11. **SQLAlchemy Core Components**

#### **Column**
```python
from sqlalchemy import Column, Integer, String
name = Column(String(100), nullable=False)
```
- Defines database table columns
- Specifies data types and constraints

#### **ForeignKey**
```python
category_id = Column(Integer, ForeignKey("categories.id"))
```
- Creates relationships between tables
- Enforces referential integrity

#### **relationship**
```python
products = relationship("Product", back_populates="category")
```
- Creates ORM-level relationships
- Enables easy navigation between related objects

#### **declarative_base**
```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```
- Base class for all model classes
- Provides ORM functionality

### 12. **Database Engine & SessionMaker**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:pass@localhost/db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Engine:** Database connection pool and configuration
**SessionMaker:** Factory for creating database sessions

---

## 🎯 When to Use What - Decision Tree

### **For API Organization:**
- Single endpoint → Direct function in main.py
- Multiple related endpoints → **APIRouter**
- Large application → Multiple APIRouters + sub-applications

### **For Data Validation:**
- Simple data → **BaseModel**
- Optional fields → **Optional[Type]**
- Lists of items → **List[Type]**
- Complex relationships → **Forward references** + **model_rebuild()**

### **For Database Operations:**
- Simple queries → **Session.query()**
- Error handling → **HTTPException**
- Common functionality → **Depends()**

### **For Database Changes:**
- Development/testing → **Base.metadata.create_all()**
- Production → **Alembic migrations**
- One-time scripts → Direct SQL with **Session.execute()**

---

## 🚨 Common Patterns & Best Practices

### **Dependency Pattern:**
```python
# Create dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use in routes
@router.get("/")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### **Error Handling Pattern:**
```python
@router.get("/{id}")
def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

### **Schema Pattern:**
```python
# Base schema (shared fields)
class ItemBase(BaseModel):
    name: str
    description: str

# Creation schema (for POST)
class ItemCreate(ItemBase):
    pass

# Response schema (for GET)
class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
```

### **Model Relationship Pattern:**
```python
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products" 
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")
```

---

## 🔍 Debugging Tips

### **Import Errors:**
```python
# ❌ Wrong - causes circular import
from schemas.product import ProductResponse

# ✅ Correct - use TYPE_CHECKING
if TYPE_CHECKING:
    from schemas.product import ProductResponse
```

### **Validation Errors:**
```python
# Check what's failing
try:
    item = ItemCreate(**data)
except ValidationError as e:
    print(e.json())  # Shows detailed error info
```

### **Database Errors:**
```python
# Check what query is being generated
query = db.query(Product).filter(Product.name == "test")
print(str(query))  # Shows actual SQL
```

### **Relationship Issues:**
```python
# Make sure back_populates match
# Product.category points to Category.products
# Category.products points to Product.category
```

---

## 🎓 Learning Path Progression

### **Beginner Level (Current):**
- ✅ FastAPI basics (APIRouter, routes)
- ✅ Pydantic (BaseModel, validation)
- ✅ SQLAlchemy (models, relationships)
- ✅ Database operations (Session, queries)

### **Intermediate Level (Next):**
- Authentication (JWT, OAuth2)
- Advanced relationships (Many-to-Many)
- File uploads
- Background tasks
- Testing (pytest)

### **Advanced Level (Future):**
- Custom middleware
- WebSockets
- Microservices
- Performance optimization
- Production deployment

---

**Remember:** Each of these tools solves a specific problem. Understanding **when** and **why** to use them is more important than memorizing syntax. Focus on the concepts, and the code will follow! 🚀