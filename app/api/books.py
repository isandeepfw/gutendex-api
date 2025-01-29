from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from typing import Optional, List
import math

from .. import models, schemas, crud
from ..database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/books", response_model=schemas.BookListResponse)
def get_books(
        gutenberg_ids: Optional[str] = Query(None),
        languages: Optional[str] = Query(None),
        mime_types: Optional[str] = Query(None),
        topic: Optional[str] = Query(None),
        author: Optional[str] = Query(None),
        title: Optional[str] = Query(None),
        limit: int = Query(25, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    # Parse comma-separated parameters
    filters = {
        "gutenberg_ids": [int(id) for id in gutenberg_ids.split(",")] if gutenberg_ids else None,
        "languages": languages.split(",") if languages else None,
        "mime_types": mime_types.split(",") if mime_types else None,
        "topics": topic.split(",") if topic else None,
        "authors": author.split(",") if author else None,
        "title_terms": title.split(",") if title else None
    }

    books, total = crud.get_filtered_books(db, limit=limit, offset=offset, **filters)

    return {
        "count": total,
        "next_offset": offset + limit if offset + limit < total else None,
        "books": books
    }