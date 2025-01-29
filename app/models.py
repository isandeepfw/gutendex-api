from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

from sqlalchemy import Table, Column, Integer, ForeignKey
from .database import Base

# Association table for many-to-many relationship between Book and Author
books_book_authors = Table(
    "books_book_authors",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", Integer, ForeignKey("books_book.id")),
    Column("author_id", Integer, ForeignKey("books_author.id"))
)

# Association table for many-to-many relationship between Book and Language
books_book_languages = Table(
    "books_book_languages",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", Integer, ForeignKey("books_book.id")),
    Column("language_id", Integer, ForeignKey("books_language.id"))
)

# Association table for many-to-many relationship between Book and Subject
books_book_subjects = Table(
    "books_book_subjects",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", Integer, ForeignKey("books_book.id")),
    Column("subject_id", Integer, ForeignKey("books_subject.id"))
)

# Association table for many-to-many relationship between Book and Bookshelf
books_book_bookshelves = Table(
    "books_book_bookshelves",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", Integer, ForeignKey("books_book.id")),
    Column("bookshelf_id", Integer, ForeignKey("books_bookshelf.id"))
)

class Author(Base):
    __tablename__ = "books_author"
    id = Column(Integer, primary_key=True)
    birth_year = Column(Integer)
    death_year = Column(Integer)
    name = Column(String(128))
    # Relationship to Book (many-to-many)
    books = relationship("Book", secondary="books_book_authors", back_populates="authors")

class Book(Base):
    __tablename__ = "books_book"
    id = Column(Integer, primary_key=True, index=True)
    download_count = Column(Integer)
    gutenberg_id = Column(Integer)
    media_type = Column(String(16))
    title = Column(String)

    # Relationships
    authors = relationship("Author", secondary="books_book_authors", back_populates="books")
    languages = relationship("Language", secondary="books_book_languages", back_populates="books")
    subjects = relationship("Subject", secondary="books_book_subjects", back_populates="books")
    bookshelves = relationship("Bookshelf", secondary="books_book_bookshelves", back_populates="books")
    formats = relationship("Format", back_populates="book")

class Language(Base):
    __tablename__ = "books_language"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(4))

    # Relationship to Book (many-to-many)
    books = relationship("Book", secondary="books_book_languages", back_populates="languages")

class Subject(Base):
    __tablename__ = "books_subject"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    # Relationship to Book (many-to-many)
    books = relationship("Book", secondary="books_book_subjects", back_populates="subjects")

class Bookshelf(Base):
    __tablename__ = "books_bookshelf"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    # Relationship to Book (many-to-many)
    books = relationship("Book", secondary="books_book_bookshelves", back_populates="bookshelves")

class Format(Base):
    __tablename__ = "books_format"
    id = Column(Integer, primary_key=True, index=True)
    mime_type = Column(String(32))
    url = Column(String)
    book_id = Column(Integer, ForeignKey("books_book.id"))

    # Relationship to Book (one-to-many)
    book = relationship("Book", back_populates="formats")
