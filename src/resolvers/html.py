import re
import urllib.request
from urllib.parse import urljoin

# Common media extensions
MEDIA_EXTENSIONS = (
    # Video formats
    ".mp4", ".webm", ".mov",
    # Audio formats
    ".mp3",  ".wav", ".ogg", ".flac",
    # Image formats
    ".png", ".jpg", ".jpeg", ".gif", ".webp"
)

# Regex patterns for media URLs
SRC_REGEX = re.compile(
    r'''(?:src|href)=["']([^"']+)["']''', # Matches src or href attributes
    re.IGNORECASE # Case-insensitive matching
)

def resolve(url, timeout=10):
    """
    Attempts to extract direct media URLs from an HTML page.
    Returns a list of absolute URLs.
    """
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "rawget/0.1"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as res:
            content_type = res.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                return []

            html = res.read().decode(errors="ignore")
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return []

    matches = SRC_REGEX.findall(html)
    results = []

    for match in matches:
        lower = match.lower()
        if any(lower.endswith(ext) for ext in MEDIA_EXTENSIONS):
            absolute = urljoin(url, match)
            results.append(absolute)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for r in results:
        if r not in seen:
            seen.add(r)
            unique.append(r)

    return unique
