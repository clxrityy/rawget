import pytest
import os
from pathlib import Path
from src.download import download_file

options = {
    "url": "",
    "file_name": "",
    "expected_suffix": "",
    "expected_download": Path("")
}

# Helper function to test downloading files
#   - The file should be placed in the expected download location
#   - The file should have the correct extension
#   - The file should have non-zero size
#   - The file should be removed after the test
@pytest.mark.skip
def test_download(capsys: pytest.CaptureFixture[str], opts: dict = options):

    url = opts["url"]
    file_name = opts["file_name"]
    expected_suffix = opts["expected_suffix"]
    expected_download = opts["expected_download"]

    try:
        download_file(url, file_name)
        captured = capsys.readouterr()
        assert "Downloaded" in captured.out, f"Expected 'Downloading' message in output, got: {captured.out}"
        assert expected_download.exists(), f"Expected file {expected_download} to exist"
        assert expected_download.suffix == expected_suffix, f"Expected file {expected_download} to have {expected_suffix} extension"
        assert expected_download.stat().st_size > 0, f"Expected file {expected_download} to have non-zero size"
    except Exception as e:
        assert False, f"Download failed with exception: {e}"
    finally:
        if expected_download.exists():
            os.remove(expected_download)
        assert not expected_download.exists(), f"Expected file {expected_download} to be removed"
