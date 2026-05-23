
from fastapi import APIRouter, status
from src.books.book_data import books
from src.books.schemas import Book,UpdateBook
from typing import List

book_router= APIRouter()

@book_router.get('/',response_model=List[Book])
async def get_all_book():
    return books

@book_router.post('/')
async def create_book(book_data:Book):
    new_book=book_data.model_dump()
    books.book_routerend(new_book)
    return new_book

   
@book_router.get('/{book_id}')
async def get_book_byid(book_id:int):
    for book in books:
        if book['id']==book_id:
            return book
    return "Book not found"

@book_router.patch('/{book_id}')
async def update_book(book_id:int,update_data:UpdateBook):
    for book in books:
        if book['id']==book_id:
            book['title']=update_data.title
            book['author']=update_data.author
            book['year']=update_data.year
            return book
    return "Book not found"


@book_router.delete('/{book_id}')
async def get_book_byid(book_id:int):
    for book in books:
        if book['id']==book_id:
            books.remove(book)
            return "Book deleted"
    return "Book not found"
