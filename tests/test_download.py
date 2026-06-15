from conftest import test_download, mock_download_dir, temp_download_dir

def test_get_default_download_dir():
    dir_path = mock_download_dir or temp_download_dir
    assert dir_path is not None

png_url = "https://avatars.githubusercontent.com/u/97744702?v=4"
mp3_url = "https://github.com/clxrityy/clxrity.xyz/blob/wav/public/assets/audio/previews/dreamy-guitar-loop.mp3"
wav_url = "https://github.com/clxrityy/clxrity.xyz/blob/wav/public/assets/audio/yearbook/awards/bring-it-in-%5B87%5D.wav"
webp_url = "https://github.com/clxrityy/clxrity.xyz/blob/wav/public/assets/img/musictable.webp"

# Test downloading a PNG file with default behavior
#   - The file should be placed in the default download directory
def test_download_file_default_behavior(capsys, mock_download_dir):
    expected_download = mock_download_dir / "default.png"
    opts = {
        "url": png_url,
        "file_name": "default.png",
        "expected_suffix": ".png",
        "expected_download": expected_download
    }
    test_download(capsys, opts)


# Test downloading a PNG file with a leading slash in the filename
#   - The leading slash should be ignored and the file should be placed in the default download directory
def test_download_file_ignore_leading_slash(capsys, mock_download_dir):
    expected_download = mock_download_dir / "default.png"
    opts = {
        "url": png_url,
        "file_name": "/default.png",
        "expected_suffix": ".png",
        "expected_download": expected_download
    }
    test_download(capsys, opts)

# Test downloading a PNG file to a temporary directory
#   - The file should be placed in the specified temporary directory
def test_download_file_temp_dir(capsys, mock_download_dir):
    output_path = "subdir/default.png"
    expected_download = mock_download_dir / output_path
    opts = {
        "url": png_url,
        "file_name": output_path,
        "expected_suffix": ".png",
        "expected_download": expected_download
    }
    test_download(capsys, opts)

# Test downloading MP3 file
def test_download_mp3_file(capsys, mock_download_dir):
    expected_download = mock_download_dir / "default.mp3"
    opts = {
        "url": mp3_url,
        "file_name": "default.mp3",
        "expected_suffix": ".mp3",
        "expected_download": expected_download
    }
    test_download(capsys, opts)

# Test downloading WAV file
def test_download_wav_file(capsys, mock_download_dir):
    expected_download = mock_download_dir / "default.wav"
    opts = {
        "url": wav_url,
        "file_name": "default.wav",
        "expected_suffix": ".wav",
        "expected_download": expected_download
    }
    test_download(capsys, opts)

# Test downloading WEBP file
def test_download_webp_file(capsys, mock_download_dir):
    expected_download = mock_download_dir / "default.webp"
    opts = {
        "url": webp_url,
        "file_name": "default.webp",
        "expected_suffix": ".webp",
        "expected_download": expected_download
    }
    test_download(capsys, opts)
