import pickle
import pandas as pd
from urllib.parse import urlparse
from url_feature_extractor import extract_model_features

MODEL_PATH = "model/phishing_model.pkl"

FEATURE_COLUMNS = [
    "UsingIP",
    "LongURL",
    "ShortURL",
    "Symbol@",
    "Redirecting//",
    "PrefixSuffix-",
    "SubDomains",
    "HTTPS",
    "DomainRegLen",
    "Favicon",
    "NonStdPort",
    "HTTPSDomainURL",
    "RequestURL",
    "AnchorURL",
    "LinksInScriptTags",
    "ServerFormHandler",
    "InfoEmail",
    "AbnormalURL",
    "WebsiteForwarding",
    "StatusBarCust",
    "DisableRightClick",
    "UsingPopupWindow",
    "IframeRedirection",
    "AgeofDomain",
    "DNSRecording",
    "WebsiteTraffic",
    "PageRank",
    "GoogleIndex",
    "LinksPointingToPage",
    "StatsReport"
]

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "account", "bank",
    "paypal", "signin", "password", "update", "confirm",
    "gift", "free", "claim", "reward"
]

TRUSTED_DOMAINS = [
    "google.com",
    "amazon.in",
    "amazon.com",
    "wikipedia.org",
    "microsoft.com",
    "apple.com",
    "github.com",
    "openai.com",
    "youtube.com",
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "paypal.com"
]


def load_model():
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)


def extract_domain(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def is_trusted_domain(domain: str) -> bool:
    return domain in TRUSTED_DOMAINS or any(domain.endswith("." + d) for d in TRUSTED_DOMAINS)


def calculate_rule_risk(url: str, features: dict):
    url_lower = url.lower()
    score = 0
    reasons = []

    if features["Symbol@"] == 1:
        score += 3
        reasons.append("Contains @ symbol")

    if features["PrefixSuffix-"] == 1:
        score += 2
        reasons.append("Hyphenated domain")

    if features["HTTPS"] == -1:
        score += 2
        reasons.append("Does not use HTTPS")

    if features["UsingIP"] == 1:
        score += 3
        reasons.append("Uses IP address in domain")

    if features["ShortURL"] == 1:
        score += 2
        reasons.append("Uses URL shortener")

    if features["Redirecting//"] == 1:
        score += 2
        reasons.append("Suspicious redirect pattern")

    if features["HTTPSDomainURL"] == 1:
        score += 2
        reasons.append("Contains 'https' inside domain")

    if features["StatsReport"] == 1:
        score += 2
        reasons.append("Contains suspicious phishing keywords")

    keyword_hits = [word for word in SUSPICIOUS_KEYWORDS if word in url_lower]
    if keyword_hits:
        score += min(4, len(keyword_hits))
        reasons.append(f"Suspicious keywords found: {', '.join(keyword_hits)}")

    if len(url) > 75:
        score += 2
        reasons.append("Very long URL")

    return score, reasons


def final_decision(url: str, model_prediction: int, probabilities, rule_score: int, reasons: list):
    domain = extract_domain(url)
    trusted = is_trusted_domain(domain)

    phishing_prob = probabilities[1] * 100
    legit_prob = probabilities[0] * 100

    # Trusted domain over HTTP only -> Suspicious, not Phishing
    if trusted and url.startswith("http://") and rule_score <= 2:
        return "Suspicious", max(60.0, phishing_prob)

    # Strong phishing cases
    if rule_score >= 5:
        return "Phishing", max(85.0, min(95.0, 55 + rule_score * 5))

    if model_prediction == 1 and phishing_prob >= 80 and not trusted:
        return "Phishing", phishing_prob

    # Moderate-risk cases
    if rule_score >= 2:
        return "Suspicious", max(55.0, phishing_prob)

    if model_prediction == 1 and phishing_prob < 80:
        return "Suspicious", phishing_prob

    return "Legitimate", legit_prob

def main():
    model = load_model()

    url = input("Enter URL: ").strip()
    features = extract_model_features(url)

    input_df = pd.DataFrame(
        [[features[col] for col in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )

    model_prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    rule_score, reasons = calculate_rule_risk(url, features)
    label, confidence = final_decision(url, model_prediction, probabilities, rule_score, reasons)

    print("\nExtracted Features:")
    for key, value in features.items():
        print(f"{key}: {value}")

    print("\n===== Model Output =====")
    print("Model Prediction :", "Phishing" if model_prediction == 1 else "Legitimate")
    print(
        f"Model Probabilities -> Legitimate: {probabilities[0] * 100:.2f}%, "
        f"Phishing: {probabilities[1] * 100:.2f}%"
    )

    print("\n===== Rule Analysis =====")
    print("Rule Risk Score:", rule_score)
    if reasons:
        print("Reasons:")
        for reason in reasons:
            print(f"- {reason}")
    else:
        print("Reasons: None")

    print("\n===== Final Prediction =====")
    print("URL:", url)
    print("Prediction :", label)
    print(f"Confidence : {confidence:.2f}%")

    if label == "Suspicious":
        print("Advice     : Check the URL carefully before visiting.")
    elif label == "Phishing":
        print("Advice     : Avoid visiting this website.")
    else:
        print("Advice     : Appears safe based on current checks.")


if __name__ == "__main__":
    main()