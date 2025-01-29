from fastapi import FastAPI
from .api import books  # Import the books router

app = FastAPI()

# Include the books router with the /api prefix
app.include_router(books.router, prefix="/api")
