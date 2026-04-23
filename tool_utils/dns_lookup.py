import socket
from urllib.parse import urlparse

def get_domain(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    parsed = urlparse(url)
    return parsed.netloc

def dns_lookup(url):
    try:
        domain = get_domain(url)
        ip = socket.gethostbyname(domain)
        return {
            "domain": domain,
            "ip_address": ip
        }
    except Exception as e:
        return {
            "error": str(e)
        }