from typing import Dict, List

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
HEADERS = {"User-Agent": ua.random}


async def scrape_quotes(
    base_url: str, page_count: int, max_quotes: int
) -> List[Dict[str, List[str]]]:
    quotes_data = []
    async with httpx.AsyncClient(headers=HEADERS, timeout=None) as client:
        for page in range(1, page_count + 1):
            url = f"{base_url}?page={page}"
            response = await client.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            quote_blocks = soup.find_all("div", class_="quoteDetails")
            for quote_block in quote_blocks:
                quote_text_tag = quote_block.find("div", class_="quoteText")
                if not quote_text_tag:
                    continue

                author_tag = quote_block.find("span", class_="authorOrTitle")
                tag_container = quote_block.find("div", class_="greyText")

                quote_text = quote_text_tag.text.strip().split("\n")[0].strip("“”")

                author = author_tag.text.strip() if author_tag else "Unknown Author"
                tags = (
                    [tag.text.strip() for tag in tag_container.find_all("a")]
                    if tag_container
                    else []
                )

                quotes_data.append(
                    {
                        "quote": quote_text,
                        "author": author,
                        "tags": tags,
                    }
                )
    return quotes_data[:max_quotes]
