import pickle
import pandas as pd
from url_feature_extractor import extract_model_features

MODEL_PATH = "model/phishing_model.pkl"

FEATURE_COLUMNS = [
    "UsingIP","LongURL","ShortURL","Symbol@","Redirecting//","PrefixSuffix-",
    "SubDomains","HTTPS","DomainRegLen","Favicon","NonStdPort","HTTPSDomainURL",
    "RequestURL","AnchorURL","LinksInScriptTags","ServerFormHandler","InfoEmail",
    "AbnormalURL","WebsiteForwarding","StatusBarCust","DisableRightClick",
    "UsingPopupWindow","IframeRedirection","AgeofDomain","DNSRecording",
    "WebsiteTraffic","PageRank","GoogleIndex","LinksPointingToPage","StatsReport"
]

# Load model
model = pickle.load(open(MODEL_PATH, "rb"))

# RULE RISK CALCULATION
def calculate_rule_risk(features: dict):
    score = 0

    if features["Symbol@"] == 1:
        score += 3
    if features["PrefixSuffix-"] == 1:
        score += 2
    if features["HTTPS"] == -1:
        score += 2
    if features["UsingIP"] == 1:
        score += 3
    if features["ShortURL"] == 1:
        score += 2
    if features["Redirecting//"] == 1:
        score += 2
    if features["HTTPSDomainURL"] == 1:
        score += 2
    if features["StatsReport"] == 1:
        score += 2

    return score

# FINAL DECISION LOGIC
def final_decision(url, model_prediction, probabilities, rule_score):

    url_lower = url.lower()

    phishing_prob = probabilities[1] * 100
    legit_prob = probabilities[0] * 100

    # 🔴 PHISHING (strong signals)
    if (
        rule_score >= 7 or
        "@" in url_lower or
        "bank" in url_lower or
        "paypal" in url_lower or
        phishing_prob >= 85
    ):
        return "Phishing", max(phishing_prob, 85.0)

    # 🟡 SUSPICIOUS (medium signals)
    elif (
        rule_score >= 3 or
        any(x in url_lower for x in [
            "login", "verify", "update",
            "secure", "account", "confirm",
            "free", "gift", "claim"
        ])
    ):
        return "Suspicious", min(max(phishing_prob, 60.0), 75.0)

    # 🟢 LEGITIMATE
    else:
        return "Legitimate", legit_prob

# MAIN PREDICTION FUNCTION
def predict_url(url):

    features = extract_model_features(url)

    input_df = pd.DataFrame(
        [[features[col] for col in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )

    model_prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    rule_score = calculate_rule_risk(features)

    label, confidence = final_decision(
        url,
        model_prediction,
        probabilities,
        rule_score
    )

    confidence = float(round(confidence, 2))

    # Risk levels
    if label == "Legitimate":
        risk_level = "Low"
    elif label == "Suspicious":
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "prediction": label,
        "confidence": confidence,
        "risk_level": risk_level
    }
