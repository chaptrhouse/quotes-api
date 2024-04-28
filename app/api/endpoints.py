from typing import Optional

from config import settings
from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from models import Quote, QuotesResponse
from services.scraper import scrape_quotes

router = APIRouter()


@router.get("/quotes", response_model=QuotesResponse, tags=["Quotes"])
@cache(expire=settings.cache_expire)
async def get_quotes(
    category: Optional[str] = Query(None, enum=["popular", "recent", "new"]),
    page_count: int = Query(1, description="Number of pages to fetch"),
    max_quotes: int = Query(10, description="Maximum number of quotes to return"),
):
    urls = {
        "popular": "https://www.goodreads.com/quotes?page=1",
        "recent": "https://www.goodreads.com/quotes/recently_added",
        "new": "https://www.goodreads.com/quotes/recently_created",
    }
    url = urls.get(category, urls["popular"])

    quotes = await scrape_quotes(url, page_count, max_quotes)

    return QuotesResponse(
        quotes=[
            Quote(
                quote=d["quote"],
                author=d["author"],
                tags=d["tags"],
            )
            for d in quotes
        ]
    )
