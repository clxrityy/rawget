from urllib.parse import urlparse
import ipaddress
import socket
from .resolvers import resolve

def process_url(url: str) -> list[str]:
    # Reject unsafe input URL before any outbound request.
    if not is_safe_url(url):
        return []

    #  HTML resolver first
    # resolved = html_resolve(url)
    # if resolved:
    #     return resolved
    # return [url]
    resolved = resolve(url)
    # print("Resolved URLs:")
    # for item in resolved[:20]:  # Show only the first 20 for brevity
    #     print(f" - {item}")
    if resolved:
        return [item for item in resolved if is_safe_url(item)]
    return [url]

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
