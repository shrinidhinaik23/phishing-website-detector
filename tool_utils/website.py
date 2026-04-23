import whois
from datetime import datetime
from urllib.parse import urlparse


def get_domain(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    parsed = urlparse(url)
    return parsed.netloc


def get_website_age(url):
    try:
        domain = get_domain(url)
        info = whois.whois(domain)
        creation_date = info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            if creation_date.tzinfo is not None:
                now_time = datetime.now(creation_date.tzinfo)
            else:
                now_time = datetime.now()

            age_days = (now_time - creation_date).days

            return {
                "domain": domain,
                "creation_date": creation_date,
                "age_days": age_days
            }
        else:
            return {"error": "Creation date not found"}

    except Exception as e:
        return {"error": str(e)}