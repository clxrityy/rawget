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
        download_dir = get_default_download_dir()
        download_dir.mkdir(parents=True, exist_ok=True)

        # Default filename derived from URL
        default_filename = Path(url).name or "download"

        if not output:
            filename = default_filename
            filepath = download_dir / filename
        else:
            # Treat any user-provided output as a path within the download directory.
            # This avoids allowing arbitrary absolute paths while preserving relative structure.
            raw = output.rstrip("/")
            # If output ends with "/", treat it as a directory under the download directory.
            is_dir = output.endswith("/")

            # Remove a single leading slash so absolute-looking paths are still rooted in download_dir.
            # e.g., "/subdir/file" -> "subdir/file"
            if raw.startswith("/"):
                raw = raw.lstrip("/")

            output_path = download_dir / raw if raw else download_dir

            if is_dir:
                # Ensure directory exists; file will be named from URL.
                output_path.mkdir(parents=True, exist_ok=True)
                filename = default_filename
                filepath = output_path / filename
            else:
                # raw may include directories and/or filename under download_dir.
                output_path.parent.mkdir(parents=True, exist_ok=True)
                filepath = output_path

        # Normalize and ensure the final path stays within download_dir
        resolved_base = download_dir.resolve()
        resolved_path = filepath.resolve()

        if hasattr(resolved_path, "is_relative_to"):
            if not resolved_path.is_relative_to(resolved_base):
                raise ValueError(f"Refusing to write outside download directory: {resolved_path}")
        else:
            try:
                resolved_path.relative_to(resolved_base)
            except ValueError:
                raise ValueError(f"Refusing to write outside download directory: {resolved_path}")

        # Apply extension if missing
        if ext and not resolved_path.name.endswith(ext):
            resolved_path = resolved_path.with_suffix(ext)

        with open(resolved_path, "wb") as f:
            f.write(data)

        print(f"Downloaded {url} to {resolved_path}")

    except Exception as e:
        print(f"Failed to download from URL {url}\n\n{e}")
        raise e
