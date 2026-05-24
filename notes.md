# FastAPI Project — Beginner's Step-by-Step Guide

A beginner-friendly guide to building a FastAPI project from scratch.
Based on the **beyond-crud** project structure.

---

## Step 1 — Install the Required Packages

Before you write any code, you need to install the libraries your project depends on.

Open your terminal in the project root and run:

```bash
pip install fastapi uvicorn pydantic pydantic-settings sqlmodel sqlalchemy
```

| Package | What it does |
| :--- | :--- |
| `fastapi` | The web framework we use to build the API |
| `uvicorn` | The server that runs your FastAPI app |
| `pydantic` | Validates and parses the shape of your data |
| `pydantic-settings` | Loads environment variables / config from `.env` files |
| `sqlmodel` | Lets you define database tables using Python classes |
| `sqlalchemy` | The engine that actually talks to the database (SQLModel builds on top of it) |

> **Tip:** Save your dependencies to a file so others can install them easily:
> ```bash
> pip freeze > requirements.txt
> ```
> Anyone cloning your project can then run `pip install -r requirements.txt`.

---

## Step 2 — Set Up the Project Structure

A well-organized project is much easier to work with as it grows. Here is the structure we use:

```
beyond-crud/
├── src/                    ← All your application code lives here
│   ├── __init__.py         ← Creates the FastAPI app and registers routers
│   ├── config.py           ← Loads environment variables (e.g., DB URL)
│   ├── books/              ← A "feature module" — all book-related code
│   │   ├── __init__.py
│   │   ├── routes.py       ← API endpoints for books
│   │   ├── schemas.py      ← Data shapes (what a Book looks like)
│   │   └── book_data.py    ← Temporary in-memory data (fake database)
│   └── db/                 ← Database connection setup
│       ├── __init__.py
│       └── main.py         ← Creates the database engine
├── .env                    ← Secret values (DB URL, API keys) — NOT committed to git
├── .gitignore              ← Tells git what files to ignore
└── requirements.txt        ← List of installed packages
```

> **Why structure it this way?**
> Grouping code by *feature* (e.g., `books/`) instead of by *type* (e.g., all routes in one file) keeps things easy to find and scale. Each feature is self-contained.

---

## Step 3 — Create the FastAPI App (`src/__init__.py`)

This is the entry point of your application. It creates the FastAPI app object and registers your routers (explained in Step 6).

```python
# src/__init__.py
from fastapi import FastAPI
from src.books.routes import book_router

version = 'v1'
app = FastAPI(version=version)

app.include_router(book_router, prefix=f"/api/{version}/books")
```

**Key concepts:**
- `FastAPI()` creates your application.
- `include_router(...)` plugs in your routes from other files (keeps this file clean).
- `prefix` means all book routes will start with `/api/v1/books`.

To run the app:

```bash
uvicorn src:app --reload
```

- `src:app` → look inside the `src` package for a variable called `app`.
- `--reload` → automatically restarts the server when you save a file (great for development).

---

## Step 4 — Define Your Data Shapes (`schemas.py`)

A **schema** defines what a piece of data must look like. We use **Pydantic's `BaseModel`** for this.

```python
# src/books/schemas.py
from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

class UpdateBook(BaseModel):
    title: str
    author: str
    year: int
```

**Why two classes?**
- `Book` is used when **creating** a book — it includes the `id`.
- `UpdateBook` is used when **editing** a book — you only update the content fields, not the `id`.

Pydantic will automatically:
- Validate incoming request data matches these types.
- Return a clear error message if something is missing or the wrong type.

---

## Step 5 — Add Some Data (`book_data.py`)

Before we have a real database, we can use a simple Python list to store data in memory. This is great for testing your endpoints quickly.

```python
# src/books/book_data.py
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 3, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 4, "title": "Brave New World", "author": "Aldous Huxley", "year": 1932},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951},
]
```

> **Note:** This data resets every time you restart the server. It is a placeholder until we connect a real database.

---

## Step 6 — Create API Endpoints with a Router (`routes.py`)

An **endpoint** is a URL path that does something when a client (browser, mobile app, etc.) hits it. A **router** groups related endpoints together.

```python
# src/books/routes.py
from fastapi import APIRouter, status
from src.books.book_data import books
from src.books.schemas import Book, UpdateBook
from typing import List

book_router = APIRouter()

# GET /api/v1/books/ → Returns all books
@book_router.get('/', response_model=List[Book])
async def get_all_books():
    return books

# POST /api/v1/books/ → Adds a new book
@book_router.post('/')
async def create_book(book_data: Book):
    new_book = book_data.model_dump()  # Converts the Pydantic model to a plain dictionary
    books.append(new_book)
    return new_book

# GET /api/v1/books/{book_id} → Returns a single book by its ID
@book_router.get('/{book_id}')
async def get_book_by_id(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    return "Book not found"

# PATCH /api/v1/books/{book_id} → Updates a book's details
@book_router.patch('/{book_id}')
async def update_book(book_id: int, update_data: UpdateBook):
    for book in books:
        if book['id'] == book_id:
            book['title'] = update_data.title
            book['author'] = update_data.author
            book['year'] = update_data.year
            return book
    return "Book not found"

# DELETE /api/v1/books/{book_id} → Removes a book
@book_router.delete('/{book_id}')
async def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return "Book deleted"
    return "Book not found"
```

**HTTP Methods at a glance:**

| Method | Purpose |
| :--- | :--- |
| `GET` | Read / Retrieve data |
| `POST` | Create new data |
| `PATCH` | Partially update existing data |
| `DELETE` | Remove data |

**`async def`** — FastAPI is built for asynchronous code. Using `async` lets your server handle many requests at the same time without blocking.

---

## Step 7 — Manage Config Securely (`.env` + `config.py`)

Never hardcode sensitive values like database URLs or API secrets directly in your code. Instead, store them in a `.env` file and load them with `pydantic-settings`.

**Create a `.env` file in your project root:**

```
# .env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
```

> **Important:** Add `.env` to your `.gitignore` so it is never committed to git.
> ```
> # .gitignore
> .env
> venv/
> __pycache__/
> ```

**Create `src/config.py` to load those values:**

```python
# src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str  # This field will be auto-loaded from the .env file

    model_config = SettingsConfigDict(
        env_file=".env",   # Tell Pydantic where to find the .env file
        extra="ignore"     # Ignore any extra variables in .env we don't declare
    )

Config = Settings()  # Create a single instance — import this anywhere you need it
```

**Usage anywhere in the project:**

```python
from src.config import Config

print(Config.DATABASE_URL)  # Safely access the value
```

---

## Step 8 — Connect to a Database (`db/main.py`)

Now we use the `DATABASE_URL` from our config to create a database **engine**. The engine is the single object that manages all connections to the database.

```python
# src/db/main.py
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True  # Prints every SQL query to the terminal — useful for debugging
    )
)
```

**What is an `AsyncEngine`?**

A standard (synchronous) engine would **pause** (block) the entire server while waiting for the database to respond. An `AsyncEngine` runs the database call in the background, so the server stays responsive and can handle other requests in the meantime. This is the right choice for FastAPI.

---

## Where You Are Now

Here is a summary of what has been built so far:

```
✅ Step 1 — Packages installed
✅ Step 2 — Project structure created
✅ Step 3 — FastAPI app created in src/__init__.py
✅ Step 4 — Data schemas defined in books/schemas.py
✅ Step 5 — In-memory data created in books/book_data.py
✅ Step 6 — CRUD endpoints created in books/routes.py
✅ Step 7 — Environment config set up with .env + config.py
✅ Step 8 — Database engine created in db/main.py
```

**What comes next:**
- Define SQLModel table models (the actual database table shapes).
- Create database sessions (a way to run queries per request).
- Replace the in-memory `books` list with real database queries.
- Add authentication (e.g., JWT tokens).
