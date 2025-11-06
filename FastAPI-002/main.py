from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import product, category

# Import models to ensure they're registered with Base
from models.category import Category
from models.product import Product
from config.database import engine, Base

# Create all tables in correct order (Base knows the dependencies)
Base.metadata.create_all(bind=engine)

# Rebuild models to resolve forward references
from schemas.category import CategoryResponse
from schemas.product import ProductResponse
CategoryResponse.model_rebuild()
ProductResponse.model_rebuild()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

@app.get("/")
def greet():
    return "This is maha who is learning fastAPI"

app.include_router(category.router)
app.include_router(product.router)