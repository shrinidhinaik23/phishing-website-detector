import ssl
import socket
from urllib.parse import urlparse

def get_domain(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    parsed = urlparse(url)
    return parsed.netloc

def check_ssl(url):
    try:
        domain = get_domain(url)
        context = ssl.create_default_context()

        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        return {
            "status": "Valid SSL Certificate Found",
            "issuer": dict(x[0] for x in cert.get("issuer", [])),
            "subject": dict(x[0] for x in cert.get("subject", [])),
        }

    except Exception as e:
        return {
            "status": f"SSL check failed: {str(e)}"
        }