from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import Optional, List
from . import models  # Import the models module
from . import schemas  # Import schemas if needed

def get_filtered_books(
        db: Session,
        gutenberg_ids: Optional[List[int]] = None,
        languages: Optional[List[str]] = None,
        mime_types: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        authors: Optional[List[str]] = None,
        title_terms: Optional[List[str]] = None,
        limit: int = 25,
        offset: int = 0
):
    base_query = db.query(models.Book)

    # Apply joins
    base_query = base_query \
        .outerjoin(models.Book.authors) \
        .outerjoin(models.Book.languages) \
        .outerjoin(models.Book.subjects) \
        .outerjoin(models.Book.bookshelves) \
        .outerjoin(models.Book.formats)

    # Apply filters
    if gutenberg_ids:
        base_query = base_query.filter(models.Book.gutenberg_id.in_(gutenberg_ids))

    if languages:
        base_query = base_query.filter(models.Language.code.in_(languages))

    if mime_types:
        base_query = base_query.filter(models.Format.mime_type.in_(mime_types))

    if topics:
        topic_filters = []
        for topic in topics:
            topic = topic.strip().lower()
            topic_filters.append(
                or_(
                    func.lower(models.Subject.name).contains(topic),
                    func.lower(models.Bookshelf.name).contains(topic)
                )
            )
        base_query = base_query.filter(or_(*topic_filters))

    if authors:
        author_filters = []
        for author in authors:
            author = author.strip().lower()
            author_filters.append(func.lower(models.Author.name).contains(author))
        base_query = base_query.filter(or_(*author_filters))

    if title_terms:
        title_filters = []
        for term in title_terms:
            term = term.strip().lower()
            title_filters.append(func.lower(models.Book.title).contains(term))
        base_query = base_query.filter(or_(*title_filters))

    # Get total count
    total = base_query.distinct().count()

    # Apply sorting and pagination
    books = base_query \
        .options(
        joinedload(models.Book.authors),
        joinedload(models.Book.languages),
        joinedload(models.Book.subjects),
        joinedload(models.Book.bookshelves),
        joinedload(models.Book.formats)
    ) \
        .order_by(models.Book.download_count.desc()) \
        .distinct() \
        .offset(offset) \
        .limit(limit) \
        .all()

    # Convert to response format
    book_responses = []
    for book in books:
        book_responses.append({
            "title": book.title,
            "authors": [{
                "name": author.name,
                "birth_year": author.birth_year,
                "death_year": author.death_year
            } for author in book.authors],
            "languages": [{"code": lang.code} for lang in book.languages],
            "subjects": [{"name": subj.name} for subj in book.subjects],
            "bookshelves": [{"name": bs.name} for bs in book.bookshelves],
            "download_links": {fmt.mime_type: fmt.url for fmt in book.formats},
            "download_count": book.download_count
        })

    return book_responses, total