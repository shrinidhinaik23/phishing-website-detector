import pickle
import pandas as pd

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


def load_model():
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    return model


def get_user_input():
    print("\nEnter feature values one by one.")
    print("Use dataset-style values like -1, 0, 1.\n")

    values = []
    for feature in FEATURE_COLUMNS:
        while True:
            try:
                value = int(input(f"{feature}: ").strip())
                values.append(value)
                break
            except ValueError:
                print("Please enter an integer value like -1, 0, or 1.")

    return pd.DataFrame([values], columns=FEATURE_COLUMNS)


def main():
    model = load_model()
    input_df = get_user_input()

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    print("\n===== Prediction Result =====")
    print("Prediction :", "Phishing" if prediction == 1 else "Legitimate")
    print(f"Confidence : {max(probability) * 100:.2f}%")
    print(f"Probabilities -> Legitimate: {probability[0] * 100:.2f}%, Phishing: {probability[1] * 100:.2f}%")


if __name__ == "__main__":
    main()