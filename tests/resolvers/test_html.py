import urllib.error
import urllib.request
from src.resolvers.html import resolve

class FakeResponse:
    def __init__(self, content_type, body):
        self.headers = {"Content-Type": content_type}
        self._body = body
    def read(self):
        return self._body.encode("utf-8")
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False

def test_resolve_extracts_media_urls(monkeypatch):
    html = """
    <html>
      <body>
        <img src="/images/pic.jpg">
        <video src="http://cdn.example.com/vid.mp4"></video>
        <a href="music/track.mp3">Download</a>
        <a href="style.css">css</a>
        <script src="/scripts/app.js"></script>
      </body>
    </html>
    """
    def fake_urlopen(req, timeout=10):
        return FakeResponse("text/html; charset=utf-8", html)
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    result = resolve("https://example.com/page")
    assert result == [
        "https://example.com/images/pic.jpg",
        "http://cdn.example.com/vid.mp4",
        "https://example.com/music/track.mp3",
    ]

def test_resolve_deduplicates(monkeypatch):
    html = """
    <img src="dup.png">
    <img src="dup.png">
    <a href="dup.png">same</a>
    """
    def fake_urlopen(req, timeout=10):
        return FakeResponse("text/html", html)
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    result = resolve("https://example.com")
    assert result == ["https://example.com/dup.png"]

def test_resolve_non_html_returns_empty(monkeypatch):
    def fake_urlopen(req, timeout=10):
        return FakeResponse("application/json", "{}")
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    assert resolve("https://example.com/api") == []

def test_resolve_network_error(monkeypatch):
    def fake_urlopen(req, timeout=10):
        raise urllib.error.URLError("boom")
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    assert resolve("https://example.com") == []

def test_resolve_ignores_non_media(monkeypatch):
    html = """
    <link href="/styles/main.css">
    <script src="/scripts/app.js"></script>
    <a href="/page.html">Page</a>
    """
    def fake_urlopen(req, timeout=10):
        return FakeResponse("text/html", html)
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    assert resolve("https://example.com") == []
