# 📝 FastAPI Blog API

A scalable and production-ready **Blog API** built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**, following clean architecture principles with a modular structure and full JWT-based authentication.

---

## 🚀 Features

- ⚡ **FastAPI** for building performant APIs
- 🗃️ **PostgreSQL** with **SQLAlchemy ORM**
- 🔄 **Alembic** for versioned database migrations
- 🧱 Clean modular structure with:
  - `routers/` (API routes)
  - `schemas/` (Pydantic request/response models)
  - `services/` (business logic)
  - `models/` (SQLAlchemy ORM models)
  - `db/` (session and connection config)
- 🔐 **JWT Authentication** with access & refresh tokens
- 🧾 Full CRUD operations: Users, Posts, Comments
- ✅ Pydantic validation for requests and responses
- 📄 Auto-generated interactive API docs via Swagger (`/docs`)

---

## 📁 Project Structure

fastapi-blog-api/
├── app/
│ ├── core/ # Core logic (auth, config, utils)
│ ├── db/ # Database connection and session management
│ ├── models/ # SQLAlchemy models
│ ├── routers/ # API route definitions
│ ├── schemas/ # Pydantic schemas (request/response)
│ ├── services/ # Business logic
│ └── main.py # FastAPI app instance
├── alembic/ # Alembic migration folder
├── alembic.ini # Alembic config
├── .env # Environment variables
├── requirements.txt # Dependencies
└── README.md # Project overview

yaml
Copy code

---

## 🔐 Authentication

- User registration & login
- Password hashing with `passlib`
- JWT-based authentication (access & refresh tokens)
- Protected routes for authenticated users

---

## 🧠 Database Schema (Simplified)

```text
Users
├── id
├── username
├── email
├── hashed_password

Posts
├── id
├── title
├── content
├── user_id (FK → Users.id)
├── created_at

Comments
├── id
├── post_id (FK → Posts.id)
├── user_id (FK → Users.id)
├── content
├── created_at
⚙️ Setup Instructions
1. Clone the repository
bash
Copy code
git clone https://github.com/yourusername/fastapi-blog-api.git
cd fastapi-blog-api
2. Create and activate a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Create and configure the .env file
env
Copy code
DATABASE_URL=postgresql://user:password@localhost:5432/blogdb
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
5. Run database migrations
bash
Copy code
alembic upgrade head
6. Start the application
bash
Copy code
uvicorn app.main:app --reload
Swagger UI: http://localhost:8000/docs

