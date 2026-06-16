from urllib.parse import urlparse
import urllib.request
import os
from .process import is_safe_url

VIDEO_EXTS = {".mp4", ".webm", ".mov"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".tiff", ".bmp", ".avif", ".heic", ".pdf"}
ICON_EXTS = {".ico", ".icon"}

# Application-controlled allowlist for outbound HEAD requests used in media selection.
# Update these hosts to match the domains this tool is expected to query.
ALLOWED_CONTENT_LENGTH_HOSTS = {
    "example.com",
}

def _is_allowed_content_length_target(url: str) -> bool:
    try:
        hostname = (urlparse(url).hostname or "").lower()
    except Exception:
        return False

    if not hostname:
        return False

    return hostname in ALLOWED_CONTENT_LENGTH_HOSTS

def classify(url: str) -> str:
    """
    Classifies a URL as "video", "audio", "image", or "other" based on its file extension.
    """
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    if ext in VIDEO_EXTS:
        return "video"
    if ext in AUDIO_EXTS:
        return "audio"
    if ext in IMAGE_EXTS:
        return "image"
    if ext in ICON_EXTS:
        return "icon"
    return "other"

PREFERENCE_ORDER = {
    "video": 100,
    "audio": 50,
    "icon": -10,
    "image": 10,
    "other": 0
}

def score(url: str) -> int:
    """
    Assigns a score to a URL based on its media type, with higher scores indicating preferred types.
    """
    media_type = classify(url)
    return PREFERENCE_ORDER.get(media_type, 0)

def content_length(url: str) -> int:
    """
    Retrieves the Content-Length of the URL for size-based selection.
    """
    if not is_safe_url(url) or not _is_allowed_content_length_target(url):
        print(f"Rejected unsafe or non-allowlisted URL for content length: {url}")
        return 0
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as response:
            return int(response.headers.get("Content-Length", 0))
    except Exception as e:
        print(f"Error fetching content length for {url}: {e}")
        return 0

def select_default(urls: list[str]) -> str | None:
    """
    Selects the best URL based on type and size. It ranks URLs first by their media type score and then by content length, preferring higher scores and larger files.
    """
    ranked = []
    for url in urls:
        if not is_safe_url(url):
            continue
        ranked.append((
            score(url),
            content_length(url),
            url
        ))

    if not ranked:
        return None

    # Highest score first, then largest file
    ranked.sort(reverse=True)
    winner = ranked[0][2]

    return winner
