import logging

import requests
from bs4 import BeautifulSoup

from src.models import Document

logger = logging.getLogger(__name__)


def load_website(url: str, timeout: int = 30) -> list[Document]:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.Timeout:
        raise ValueError(f"Request to '{url}' timed out after {timeout}s.")
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch URL '{url}': {e}")

    soup = BeautifulSoup(response.content, "lxml")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    if not text:
        raise ValueError(f"No extractable text found at '{url}'.")

    return [Document(
        text=text,
        source=url,
        source_type="website",
        metadata={"url": url},
    )]
