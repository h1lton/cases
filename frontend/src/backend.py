import httpx

from src.constants import BACKEND_BASE_URL

client = httpx.AsyncClient(base_url=BACKEND_BASE_URL, timeout=5)
