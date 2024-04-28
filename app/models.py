from typing import List

from pydantic import BaseModel


class Quote(BaseModel):
    quote: str
    author: str
    tags: List[str]


class QuotesResponse(BaseModel):
    quotes: List[Quote]
