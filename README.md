# FastAPI PostgreSQL Service

A backend service built with FastAPI, using PostgreSQL for data persistence. This project provides a set of RESTful APIs for user authentication and service management.

## 🛠️ Technology Stack

- **Language**: Python 3.9+
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Driver**: `psycopg2-binary`
- **Authentication**: JWT & Hashing (Bcrypt)

## ✨ Features

- **User Authentication**:
  - Register new users (`/user/userregister`)
  - Login (`/user/userlogin`)
- **Service Management**:
  - Create, Read, Update, Delete (CRUD) operations for services
  - Filter services by brand
  - Store service details including title, description, and images

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- PostgreSQL installed and running

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd FastAPI-postgreSQL
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv env
   # Windows
   .\env\Scripts\activate
   # Linux/Mac
   source env/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r service/requirements.txt
   ```

4. **Database Configuration:**
   - Ensure you have a PostgreSQL database named `test` created.
   - **Note**: The current configuration uses a hardcoded connection string in `service/database.py`:
     `postgresql://postgres:secret@localhost:5432/test`
   - You may need to update this string or configure your local PostgreSQL user `postgres` with password `secret` to match, or modify the code to use environment variables.

### Running the Application

Start the development server using Uvicorn:

```bash
uvicorn service.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 📚 API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: Visit `http://127.0.0.1:8000/docs` to explore and test the endpoints.
- **ReDoc**: Visit `http://127.0.0.1:8000/redoc` for an alternative documentation view.

## 📂 Project Structure

```
FastAPI-postgreSQL/
├── service/
│   ├── router/
│   │   ├── users.py      # User authentication routes
│   │   └── service.py    # Service management routes
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schema.py         # Pydantic schemas
│   ├── hashing.py        # Password hashing utility
│   ├── main.py           # Application entry point
│   └── requirements.txt  # Project dependencies
└── README.md
```
