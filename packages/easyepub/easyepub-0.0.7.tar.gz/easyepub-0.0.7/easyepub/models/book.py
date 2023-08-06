from pydantic import BaseModel


class Book(BaseModel):
    uid: str
    title: str
    author: str
    creation_date: str
    language: str
