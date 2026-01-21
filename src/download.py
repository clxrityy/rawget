import os
import urllib.request
from .extension import detect_file_extension
from pathlib import Path

def get_default_download_dir():
    # Linux (XDG spec)
    xdg = os.environ.get("XDG_DOWNLOAD_DIR")
    if xdg:
        return Path(xdg).expanduser()

    # macOS / Windows / fallback
    return Path.home() / "Downloads"

def download_file(url: str, output = None):
    try:
        with urllib.request.urlopen(url) as response:
            content_type = response.headers.get('Content-Type', '')
            data = response.read()

            ext = detect_file_extension(data, url, content_type)
            filename = output or Path(url).name or "rawget_download"
            if not filename.endswith(ext):
                filename += ext

            download_dir = get_default_download_dir()
            filepath = download_dir / filename

            with open(filepath, "wb") as f:
                f.write(data)

            print(f"Downloaded {url} to {filepath}")


    except Exception as e:
        print(f"Failed to download from URL {url}\n\n{e}")
