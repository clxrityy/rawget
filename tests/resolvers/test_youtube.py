from src.resolvers.youtube import youtube_resolve

def test_youtube_resolve():
    # Test with a known YouTube video URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    results = youtube_resolve(url)
    assert isinstance(results, list)
    assert len(results) > 0  # Expect at least one media link

def test_youtube_resolve_invalid_url():
    # Test with an invalid YouTube URL
    url = "https://www.youtube.com/watch?v=invalid"
    results = youtube_resolve(url)
    assert results == []  # Should return an empty list for invalid video IDs

def test_youtube_resolve_non_video_url():
    # Test with a non-video YouTube URL
    url = "https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ"
    results = youtube_resolve(url)
    assert results == []  # Should return an empty list for non-video URLs
