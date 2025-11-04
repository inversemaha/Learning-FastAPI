# Learning FastAPI & React 🚀

This repository is dedicated to my journey of learning **FastAPI** for backend development and **React.js** for frontend integration.

FastAPI is a modern, fast web framework for building APIs with Python 3.14+ using standard Python type hints.

React.js will be used to consume FastAPI APIs and build a dynamic frontend.

---

## 🗂 Repository Structure (Backend)

```
app/
├── main.py                # FastAPI app entrypoint
├── database.py            # Database connection and session
├── models/                # SQLAlchemy models
│   ├── product.py
│   └── category.py
├── schemas/               # Pydantic schemas for validation and response models
│   ├── product.py
│   └── category.py
└── routes/                # API routers (endpoints)
    └── product.py
```

---

## 📚 Day 1 Learning Plan (001)

Today, I have learned:

1. **FastAPI basic structure**

   * Creating `main.py` and initializing FastAPI app
   * Understanding routes, path parameters, and query parameters
   * Response models using Pydantic

2. **Pydantic Models (Schemas)**

   * `ProductCreate`, `ProductUpdate`, `ProductResponse`
   * Request validation and response serialization
   * `orm_mode=True` to work with SQLAlchemy models

3. **SQLAlchemy ORM**

   * Declarative base, creating models (`Product`)
   * Connecting to **PostgreSQL**
   * Creating tables and managing database sessions
   * Performing CRUD operations:

     * Create (`POST`)
     * Read (`GET`)
     * Update (`PUT`)
     * Delete (`DELETE`)

4. **Project Structure**

   * Using folders for `models/`, `schemas/`, `routes/`
   * Using `APIRouter` for modular API routes
   * Best practices for maintainable FastAPI project structure

**Note:** Relationships between models will be learned in future phases.

---

## 🌐 Day 2 Learning Plan: Frontend Integration

Next steps include **React.js frontend** integration:

* Create React app to consume FastAPI APIs
* Implement **CRUD operations** from frontend
* Connect React forms to FastAPI endpoints:

  * Create Product
  * List Products
  * Update Product
  * Delete Product
* Display API data dynamically using React state and components
* Optional: Add Axios for API requests

**Proposed folder structure:**

```
frontend/

```

---

## 🔧 Tools & Libraries

* **Python 3.14+**, **FastAPI**, **SQLAlchemy**, **Pydantic**
* **PostgreSQL** database
* **React.js**, **Axios** (for API calls)
* **Uvicorn** – ASGI server to run FastAPI backend
* **npm / yarn** – for frontend package management

---

## 📝 Notes & Best Practices

1. Keep **one model per file** (`product.py`, `category.py`)
2. Keep **Pydantic schemas separate** for Create, Update, Response
3. Use **APIRouter** for modular API endpoints
4. Use **dependency injection** (`Depends`) for DB sessions
5. Use `orm_mode = True` in response models
6. Follow consistent naming conventions:

   * Models → `Product`, `Category`
   * Schemas → `ProductCreate`, `ProductResponse`
   * Routers → `product.py`

---

## 🚀 Running the Project

### Backend

```bash
# Activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app.main:app --reload
```

* Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Frontend (Planned)

```bash
# Create React app
npx create-react-app frontend
cd frontend
npm start
```

* React app will communicate with FastAPI APIs via Axios.

---

## 📌 Future Enhancements

* Implement **React frontend CRUD operations**
* Add **model relationships** (Product → Category)
* Explore **asynchronous FastAPI endpoints**
* Dockerize both backend and frontend
* Add **unit tests** and API testing

---

**Happy Learning! 🚀**
*Maha’s FastAPI + React Journey*
