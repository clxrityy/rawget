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
            # ensure ext starts with a dot
            if ext and not ext.startswith("."):
                ext = f".{ext}"

        # Decide destination
        if not output:
            download_dir = get_default_download_dir()
            download_dir.mkdir(parents=True, exist_ok=True)
            filename = Path(url).name
            filepath = download_dir / filename
        elif output.startswith("/"):  # Absolute path
            cleaned = output.rstrip("/")
            # Case: only a leading slash and a filename -> treat as Downloads
            if "/" not in cleaned[1:]:
                download_dir = get_default_download_dir()
                download_dir.mkdir(parents=True, exist_ok=True)
                filename = Path(cleaned).name or Path(url).name
                filepath = download_dir / filename
            else:
                output_path = Path(cleaned)
                if output.endswith("/"):
                    output_path.mkdir(parents=True, exist_ok=True)
                    filename = Path(url).name
                    filepath = output_path / filename
                else:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    filepath = output_path
        else:
            # relative: place inside default Downloads
            base_dir = get_default_download_dir()
            output_path = (base_dir / output.rstrip("/"))
            if output.endswith("/"):
                output_path.mkdir(parents=True, exist_ok=True)
                filename = Path(url).name
                filepath = output_path / filename
            else:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                filepath = output_path

        # Apply extension if missing
        if ext and not filepath.name.endswith(ext):
            filepath = filepath.with_suffix(ext)

        with open(filepath, "wb") as f:
            f.write(data)

        print(f"Downloaded {url} to {filepath}")

    except Exception as e:
        print(f"Failed to download from URL {url}\n\n{e}")
        raise e
