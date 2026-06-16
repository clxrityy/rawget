from urllib.parse import urlparse, urlunparse
import ipaddress
import socket
from .resolvers import resolve

def process_url(url: str) -> list[str]:
    # Reject unsafe input URL before any outbound request.
    pinned_url = get_pinned_safe_url(url)
    if not pinned_url:
        return []

    #  HTML resolver first
    # resolved = html_resolve(url)
    # if resolved:
    #     return resolved
    # return [url]
    resolved = resolve(pinned_url)
    # print("Resolved URLs:")
    # for item in resolved[:20]:  # Show only the first 20 for brevity
    #     print(f" - {item}")
    if resolved:
        safe_items = []
        for item in resolved:
            pinned_item = get_pinned_safe_url(item)
            if pinned_item:
                safe_items.append(pinned_item)
        return safe_items
    return [pinned_url]

def get_pinned_safe_url(url: str) -> str | None:
    """
    Validate URL safety and return an IP-pinned URL in the form:
    scheme://original-host@validated-ip[:port]/path?query#fragment

    This avoids DNS rebinding/TOCTOU issues by ensuring outbound requests
    use the validated IP while preserving original hostname for Host/SNI.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return None

    if parsed.scheme not in ("http", "https"):
        return None

    hostname = parsed.hostname
    if not hostname:
        return None

    try:
        addrinfo_list = socket.getaddrinfo(hostname, parsed.port, type=socket.SOCK_STREAM)
    except OSError:
        return None

    public_ip = None
    for _family, _socktype, _proto, _canonname, sockaddr in addrinfo_list:
        ip_str = sockaddr[0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            continue

        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        ):
            continue
        public_ip = ip_str
        break

    if not public_ip:
        return None

    host_token = parsed.hostname or ""
    if ":" in host_token and not host_token.startswith("["):
        host_token = f"[{host_token}]"

    pinned_netloc = f"{host_token}@{public_ip}"
    if parsed.port:
        pinned_netloc = f"{pinned_netloc}:{parsed.port}"

    return urlunparse((
        parsed.scheme,
        pinned_netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))

def is_safe_url(url: str) -> bool:
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
