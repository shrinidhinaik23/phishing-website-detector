import re
from urllib.parse import urlparse


SHORTENERS = [
    "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co",
    "is.gd", "buff.ly", "adf.ly", "cutt.ly", "rebrand.ly"
]

SUSPICIOUS_WORDS = [
    "login", "verify", "update", "secure", "account", "bank",
    "confirm", "signin", "submit", "password", "free", "bonus",
    "gift", "claim", "paypal", "ebay", "webscr"
]


def safe_parse(url: str):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    parsed = urlparse(url)
    return url, parsed


def has_ip(domain: str) -> bool:
    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    return bool(re.match(ip_pattern, domain))


def count_subdomains(domain: str) -> int:
    parts = domain.split(".")
    if len(parts) <= 2:
        return 0
    return len(parts) - 2


def has_prefix_suffix(domain: str) -> bool:
    return "-" in domain


def long_url(url: str) -> int:
    length = len(url)
    if length < 54:
        return -1
    elif 54 <= length <= 75:
        return 0
    return 1


def short_url_service(domain: str) -> int:
    return 1 if any(s in domain for s in SHORTENERS) else -1


def symbol_at(url: str) -> int:
    return 1 if "@" in url else -1


def redirecting_double_slash(url: str) -> int:
    pos = url.rfind("//")
    return 1 if pos > 6 else -1


def https_feature(parsed) -> int:
    return 1 if parsed.scheme == "https" else -1


def domain_reg_len(domain: str) -> int:
    return 0


def favicon_feature(url: str) -> int:
    return 0


def non_std_port(parsed) -> int:
    if parsed.port is None:
        return -1
    return 1 if parsed.port not in [80, 443] else -1


def https_domain_url(domain: str) -> int:
    return 1 if "https" in domain else -1


def request_url(url: str) -> int:
    return 0


def anchor_url(url: str) -> int:
    return 0


def links_in_script_tags(url: str) -> int:
    return 0


def server_form_handler(url: str) -> int:
    return 0


def info_email(url: str) -> int:
    return 1 if "mailto:" in url or "email=" in url else -1


def abnormal_url(url: str, domain: str) -> int:
    return 1 if domain not in url else -1


def website_forwarding(url: str) -> int:
    return 0


def status_bar_customization(url: str) -> int:
    return 0


def disable_right_click(url: str) -> int:
    return 0


def using_popup_window(url: str) -> int:
    return 0


def iframe_redirection(url: str) -> int:
    return 0


def age_of_domain(domain: str) -> int:
    return 0


def dns_recording(domain: str) -> int:
    return 0


def website_traffic(domain: str) -> int:
    return 0


def page_rank(domain: str) -> int:
    return 0


def google_index(domain: str) -> int:
    return 0


def links_pointing_to_page(url: str) -> int:
    return 0


def stats_report(domain: str) -> int:
    suspicious = any(word in domain.lower() for word in SUSPICIOUS_WORDS)
    return 1 if suspicious else -1


def extract_model_features(url: str):
    original_url, parsed = safe_parse(url)
    domain = parsed.netloc.lower()

    subdomain_count = count_subdomains(domain)
    if subdomain_count == 0:
        subdomains_feature = -1
    elif subdomain_count == 1:
        subdomains_feature = 0
    else:
        subdomains_feature = 1

    return {
        "UsingIP": 1 if has_ip(domain) else -1,
        "LongURL": long_url(original_url),
        "ShortURL": short_url_service(domain),
        "Symbol@": symbol_at(original_url),
        "Redirecting//": redirecting_double_slash(original_url),
        "PrefixSuffix-": 1 if has_prefix_suffix(domain) else -1,
        "SubDomains": subdomains_feature,
        "HTTPS": https_feature(parsed),
        "DomainRegLen": domain_reg_len(domain),
        "Favicon": favicon_feature(original_url),
        "NonStdPort": non_std_port(parsed),
        "HTTPSDomainURL": https_domain_url(domain),
        "RequestURL": request_url(original_url),
        "AnchorURL": anchor_url(original_url),
        "LinksInScriptTags": links_in_script_tags(original_url),
        "ServerFormHandler": server_form_handler(original_url),
        "InfoEmail": info_email(original_url),
        "AbnormalURL": abnormal_url(original_url, domain),
        "WebsiteForwarding": website_forwarding(original_url),
        "StatusBarCust": status_bar_customization(original_url),
        "DisableRightClick": disable_right_click(original_url),
        "UsingPopupWindow": using_popup_window(original_url),
        "IframeRedirection": iframe_redirection(original_url),
        "AgeofDomain": age_of_domain(domain),
        "DNSRecording": dns_recording(domain),
        "WebsiteTraffic": website_traffic(domain),
        "PageRank": page_rank(domain),
        "GoogleIndex": google_index(domain),
        "LinksPointingToPage": links_pointing_to_page(original_url),
        "StatsReport": stats_report(domain),
    }