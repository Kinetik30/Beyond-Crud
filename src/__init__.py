from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app:FastAPI):
    print("app starting")
    yield
    print("app shutting down")

version ='v1'
app=FastAPI(version= version,lifespan=life_span)

app.include_router(book_router, prefix=f"/api/{version}/books")