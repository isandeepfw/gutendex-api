from pydantic import BaseModel
from typing import List, Dict, Optional

class AuthorResponse(BaseModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

class LanguageResponse(BaseModel):
    code: str

class SubjectResponse(BaseModel):
    name: str

class BookshelfResponse(BaseModel):
    name: str

class BookResponse(BaseModel):
    title: str
    authors: List[AuthorResponse]
    languages: List[LanguageResponse]
    subjects: List[SubjectResponse]
    bookshelves: List[BookshelfResponse]
    download_links: Dict[str, str]
    download_count: int

class BookListResponse(BaseModel):
    count: int
    next_offset: Optional[int] = None
    books: List[BookResponse]