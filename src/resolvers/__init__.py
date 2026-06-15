from urllib.parse import urlparse
from .generic import generic_resolve
from .youtube import youtube_resolve

def resolve(url: str) -> list[str]:
    """
    Resolves a URL to a list of media URLs. It first attempts to extract media URLs from the HTML content of the page. If no media URLs are found, it returns the original URL in a list.
    """
    host = urlparse(url).netloc.lower()

    if "youtube.com" in host or "youtu.be" in host:
        return youtube_resolve(url)

    return generic_resolve(url)
