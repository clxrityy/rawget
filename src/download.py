import os
import urllib.request
from .extension import detect_file_extension
from pathlib import Path
from urllib.parse import urlparse
import ipaddress
import socket

def get_default_download_dir():
    # Linux (XDG spec)
    xdg = os.environ.get("XDG_DOWNLOAD_DIR")
    if xdg:
        try:
            # Resolve to an absolute, normalized path and ensure it stays within the user's home directory.
            home = Path.home().resolve()
            candidate = Path(xdg).expanduser().resolve()
            # On Python 3.9+, Path has is_relative_to; fall back to relative_to for older versions.
            is_subpath = False
            if hasattr(candidate, "is_relative_to"):
                is_subpath = candidate.is_relative_to(home)
            else:
                try:
                    candidate.relative_to(home)
                    is_subpath = True
                except ValueError:
                    is_subpath = False
            if is_subpath:
                return candidate
        except Exception:
            # On any error, ignore XDG_DOWNLOAD_DIR and use the default below.
            pass

    # macOS / Windows / fallback
    return Path.home() / "Downloads"

def _is_safe_url(url: str) -> bool:
    """
    Basic SSRF mitigation: allow only http/https schemes and disallow
    destinations that resolve to private, loopback, link-local, reserved,
    or multicast IP ranges.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if parsed.scheme not in ("http", "https"):
        return False

    hostname = parsed.hostname
    if not hostname:
        return False

    try:
        addrinfo_list = socket.getaddrinfo(hostname, parsed.port, type=socket.SOCK_STREAM)
    except OSError:
        return False

    for _family, _socktype, _proto, _canonname, sockaddr in addrinfo_list:
        ip_str = sockaddr[0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            return False

        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        ):
            return False

    return True

def download_file(url: str, output = None):
    try:
        if not _is_safe_url(url):
            raise ValueError(f"Refusing to download from unsafe or invalid URL: {url}")

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
