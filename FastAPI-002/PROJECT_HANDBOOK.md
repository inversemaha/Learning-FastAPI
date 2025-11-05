# FastAPI Project Learning Handbook 📚

## 🎯 Project Overview
This is a **Product-Category Management API** built with FastAPI, PostgreSQL, and SQLAlchemy. You're learning how to build a REST API with database relationships.

---

## 📁 Project Structure

```
FastAPI-002/
├── 📁 config/           # Database configuration
│   └── database.py      # Database connection & setup
├── 📁 models/           # Database tables (SQLAlchemy ORM)
│   ├── product.py       # Product table definition
│   └── category.py      # Category table definition
├── 📁 schemas/          # Data validation (Pydantic)
│   ├── product.py       # Product request/response schemas
│   └── category.py      # Category request/response schemas
├── 📁 routes/           # API endpoints (FastAPI routes)
│   ├── product.py       # Product CRUD operations
│   └── category.py      # Category CRUD operations
├── main.py              # Application entry point
└── requirements.txt     # Dependencies
```

---

## 🏗️ Architecture Flow

```
1. 🌐 HTTP Request → 2. 🛣️ Route → 3. 📋 Schema → 4. 🗄️ Model → 5. 🐘 Database
   (Client)          (FastAPI)    (Pydantic)   (SQLAlchemy)    (PostgreSQL)
```

### How Data Flows:
1. **Client** sends HTTP request (GET, POST, PUT, DELETE)
2. **FastAPI Route** receives and processes the request
3. **Pydantic Schema** validates input/output data
4. **SQLAlchemy Model** interacts with database
5. **PostgreSQL** stores/retrieves data

---

## 🗄️ Database Design

### Tables & Relationships:
```sql
categories                    product
┌─────────────┐              ┌──────────────────┐
│ id (PK)     │◄─────────────┤ category_id (FK) │
│ name        │              │ id (PK)          │
└─────────────┘              │ name             │
                             │ description      │
                             │ price            │
                             │ quantity         │
                             └──────────────────┘
```

**Relationship:** One Category → Many Products (1:N)

---

## 🏷️ Code Components Explained

### 1. 📊 Models (`models/`)
**Purpose:** Define database table structure
```python
# models/category.py
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(197), unique=True)
    products = relationship("Product", back_populates="category")
```

**Key Concepts:**
- `Base` = SQLAlchemy base class
- `__tablename__` = actual database table name
- `Column()` = table columns with data types
- `relationship()` = connects tables together

### 2. 📋 Schemas (`schemas/`)
**Purpose:** Validate data going in/out of API
```python
# schemas/category.py
class CategoryCreate(CategoryBase):    # For POST requests
    pass

class CategoryResponse(CategoryBase):   # For API responses
    id: int
    products: List["ProductResponse"] = []
```

**Key Concepts:**
- `CategoryBase` = shared fields
- `CategoryCreate` = validation for new categories
- `CategoryResponse` = what client receives back
- Forward references `"ProductResponse"` prevent circular imports

### 3. 🛣️ Routes (`routes/`)
**Purpose:** Define API endpoints and business logic
```python
# routes/category.py
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    db_categories = db.query(CategoryModel).all()
    return db_categories
```

**Key Concepts:**
- `@router.get("/")` = HTTP GET endpoint
- `response_model` = what data structure to return
- `Depends(get_db)` = dependency injection for database
- `db.query()` = SQLAlchemy database operations

### 4. ⚙️ Configuration (`config/database.py`)
**Purpose:** Database connection setup
```python
db_url = "postgresql://postgres:1@localhost:5432/mahaFastAPI"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
```

---

## 🔄 Request/Response Flow Example

### Creating a New Category:

```
1. POST /categories
   Body: {"name": "Electronics"}

2. Route receives request
   ↓
3. Pydantic validates: CategoryCreate schema
   ↓  
4. SQLAlchemy creates: Category model instance
   ↓
5. Database saves: INSERT INTO categories...
   ↓
6. Response sent: CategoryResponse schema
   {"id": 1, "name": "Electronics", "products": []}
```

---

## 🔗 Understanding Relationships

### Database Level:
```sql
-- Foreign Key Constraint
product.category_id → categories.id
```

### SQLAlchemy Level:
```python
# In Product model
category_id = Column(Integer, ForeignKey("categories.id"))
category = relationship("Category", back_populates="products")

# In Category model  
products = relationship("Product", back_populates="category")
```

### What `back_populates` Does:
- **Product side:** `category` → points to Category model's `products` attribute
- **Category side:** `products` → points to Product model's `category` attribute
- Creates **bidirectional relationship**

### Usage:
```python
# Get category of a product
product = db.query(Product).first()
print(product.category.name)  # "Electronics"

# Get all products in a category
category = db.query(Category).first() 
print(len(category.products))  # 5 products
```

---

## 📝 API Endpoints

### Category Endpoints:
| Method | URL | Purpose | Request Body | Response |
|--------|-----|---------|--------------|----------|
| GET | `/categories` | Get all categories | None | List of categories |
| POST | `/categories` | Create category | `{"name": "..."}` | New category |
| GET | `/categories/{id}` | Get specific category | None | Single category |

### Product Endpoints:
| Method | URL | Purpose | Request Body | Response |
|--------|-----|---------|--------------|----------|
| GET | `/products` | Get all products | None | List of products |
| POST | `/products` | Create product | Product data | New product |
| GET | `/products/{id}` | Get specific product | None | Single product |
| PUT | `/products/{id}` | Update product | Updated data | Modified product |
| DELETE | `/products/{id}` | Delete product | None | Success message |

---

## 🚀 How to Run & Test

### 1. Start the Application:
```bash
cd FastAPI-002
uvicorn main:app --reload
```

### 2. View API Documentation:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 3. Test Endpoints:
```bash
# Create a category
curl -X POST "http://localhost:8000/categories" \
     -H "Content-Type: application/json" \
     -d '{"name": "Electronics"}'

# Create a product
curl -X POST "http://localhost:8000/products" \
     -H "Content-Type: application/json" \
     -d '{"name": "Laptop", "price": 999.99, "quantity": 10, "category_id": 1}'
```

---

## 🐛 Common Issues & Solutions

### 1. **Foreign Key Error:**
```
NoReferencedTableError: Foreign key could not find table 'categories'
```
**Solution:** Create tables in correct order (categories first, then products)

### 2. **Column Does Not Exist:**
```
UndefinedColumn: column product.category_id does not exist
```
**Solution:** Add missing column or recreate tables

### 3. **Circular Import Error:**
```
PydanticUserError: not fully defined
```
**Solution:** Use forward references `"ModelName"` and call `model_rebuild()`

### 4. **Wrong Query:**
```
AttributeError: 'Product' object has no attribute 'Product'
```
**Solution:** Use `ProductModel` not `ProductModel.Product`

---

## 📚 Key Learning Points

### 1. **MVC Pattern:**
- **Models** = Data structure (database)
- **Views** = Routes (API endpoints)  
- **Controllers** = Business logic (in route functions)

### 2. **Database Relationships:**
- **One-to-Many:** One category has many products
- **Foreign Keys:** Link tables together
- **ORM Relationships:** Navigate between related objects

### 3. **Data Validation:**
- **Input validation:** Pydantic schemas check incoming data
- **Output serialization:** Convert database objects to JSON
- **Type hints:** Help with IDE support and documentation

### 4. **Dependency Injection:**
- `Depends(get_db)` provides database session
- Automatic cleanup when request finishes
- Makes testing easier

---

## 🎓 Next Steps to Learn

1. **Authentication & Authorization** (JWT tokens)
2. **Advanced Relationships** (Many-to-Many)
3. **Database Migrations** (Alembic)
4. **Testing** (pytest, test database)
5. **Deployment** (Docker, cloud platforms)
6. **Caching** (Redis)
7. **Background Tasks** (Celery)

---

## 🔧 Useful Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --port 8000

# Check database tables (PostgreSQL)
psql -U postgres -d mahaFastAPI
\dt  # List tables
\d product  # Describe product table

# Generate requirements
pip freeze > requirements.txt
```

---

**Remember:** This project teaches you the fundamentals of building REST APIs with proper database relationships. Each component has a specific purpose, and understanding how they work together is key to building scalable applications! 🚀