from urllib.parse import urlparse
from .generic import generic_resolve
from .youtube import youtube_resolve

def resolve(url: str) -> list[str]:
    """
    Resolves a URL to a list of media URLs. It first attempts to extract media URLs from the HTML content of the page. If no media URLs are found, it returns the original URL in a list.
    """
    host = (urlparse(url).hostname or "").lower()

    if host in ("youtube.com", "youtu.be") or host.endswith(".youtube.com") or host.endswith(".youtu.be"):
        return youtube_resolve(url)

    return generic_resolve(url)
