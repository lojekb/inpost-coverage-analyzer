import aiohttp
import asyncio
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)
BASE_URL = "https://api-global-points.easypack24.net/v1/points"

async def fetch_page(session: aiohttp.ClientSession, page: int, per_page: int, country_code: str, semaphore: asyncio.Semaphore) -> List[Dict]:
    async with semaphore:
        params = {"page": page, "per_page": per_page, "country_code": country_code}
        async with session.get(BASE_URL, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            return data.get("items", [])

async def fetch_all_pages_async(country_code: str = "PL", max_pages: Optional[int] = None) -> List[Dict]:
    per_page = 500
    points = []
    semaphore = asyncio.Semaphore(50)

    async with aiohttp.ClientSession() as session:
        params = {"page": 1, "per_page": per_page, "country_code": country_code}
        async with session.get(BASE_URL, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            
            points.extend(data.get("items", []))
            total_pages = data.get("total_pages", 1)
            
            if max_pages:
                total_pages = min(total_pages, max_pages)

        if total_pages > 1:
            tasks = [
                fetch_page(session, page, per_page, country_code, semaphore)
                for page in range(2, total_pages + 1)
            ]
            results = await asyncio.gather(*tasks)
            for res in results:
                points.extend(res)

    return points