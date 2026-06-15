from src.selection import score, content_length, select_default

def test_score():
    assert score("https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_480_1_5MG.mp4") == 100
    assert score("https://file-examples.com/index.php/sample-audio-files/sample-wav-download/storage/2017/04/file_example_WAV_1MG.wav") == 50
    assert score("http://clxrity.xyz/favicon-32x32.png") == 10
    assert score("http://clxrity.xyz/favicon.ico") == -10
    assert score("https://file-examples.com/index.php/sample-documents-download/sample-pdf-download/") == 0

def test_content_length():
    # This test assumes that the URL is accessible and has a known content length.
    # In a real test, you would mock urllib.request.urlopen to return a controlled response.
    url = "http://example.com/testfile"
    length = content_length(url)
    assert isinstance(length, int)
    assert length >= 0

def test_select_default():
    urls = [
        "http://clxrity.xyz/favicon-32x32.png",
        "https://file-examples.com/index.php/sample-audio-files/sample-wav-download/storage/2017/04/file_example_WAV_1MG.wav",
        "https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_480_1_5MG.mp4",
        "http://clxrity.xyz/favicon.ico",
    ]
    selected = select_default(urls)
    assert selected == "https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_480_1_5MG.mp4"  # Assuming it has the highest score and content length
