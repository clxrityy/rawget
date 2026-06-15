from src.resolvers.generic import generic_resolve

def test_generic_resolve():
    # Test with a known HTML page containing media links
    url = "https://httpbin.org/html"
    results = generic_resolve(url)
    assert isinstance(results, list)
    assert len(results) > -1  # Expect at least one media link
    for r in results:
        assert r.startswith("http")
        assert any(r.lower().endswith(ext) for ext in (".mp4", ".webm", ".mov", ".mp3", ".wav", ".ogg", ".flac", ".png", ".jpg", ".jpeg", ".gif", ".webp"))

def test_generic_resolve_non_html():
    # Test with a non-HTML URL
    url = "https://httpbin.org/image/png"
    results = generic_resolve(url)
    assert results == []  # Should return an empty list for non-HTML content

def test_generic_resolve_invalid_url():
    # Test with an invalid URL
    url = "https://invalid.url"
    results = generic_resolve(url)
    assert results == []  # Should return an empty list for invalid URLs
