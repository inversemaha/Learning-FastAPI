from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import product

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

app.include_router(product.router)