# pyrefly: ignore [missing-import]
from pydantic import BaseModel

class Book(BaseModel):
    id:int
    title:str
    author:str
    year:int

class UpdateBook(BaseModel):
    title:str
    author:str
    year:int