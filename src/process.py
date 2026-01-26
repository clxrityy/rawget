from urllib.parse import urlparse
import ipaddress
import socket
from resolvers import html_resolve

def process_url(url: str) -> str:
    #  HTML resolver first
    resolved = html_resolve(url)
    if resolved:
        return resolved[0]
    return url

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
