from src.process import is_safe_url, process_url

def test_is_safe_url():
    assert is_safe_url("https://example.com") is True
    assert is_safe_url("http://example.com") is True
    assert is_safe_url("ftp://example.com") is False
    assert is_safe_url("javascript:alert('XSS')") is False
