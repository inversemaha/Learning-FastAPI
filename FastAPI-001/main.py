from fastapi import FastAPI
from routes import product

app = FastAPI()

@app.get("/")
def greet():
    return "This is maha who is learning fastAPI"

app.include_router(product.router)