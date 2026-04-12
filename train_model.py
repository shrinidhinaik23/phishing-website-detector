import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

DATASET_PATH = "dataset/phishing.csv"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "phishing_model.pkl")


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    print("Columns found in dataset:")
    print(df.columns.tolist())

    # Drop Index column if present
    if "Index" in df.columns:
        df = df.drop(columns=["Index"])

    # Rename label column
    if "Result" in df.columns:
        df = df.rename(columns={"Result": "label"})
    elif "class" in df.columns:
        df = df.rename(columns={"class": "label"})

    if "label" not in df.columns:
        raise ValueError("Dataset must contain a label column such as 'Result' or 'class'.")

    # Correct mapping for this dataset:
    # -1 = phishing -> 1
    #  1 = legitimate -> 0
    df["label"] = df["label"].apply(lambda x: 1 if x == -1 else 0)

    return df


def evaluate_model(model, x_test, y_test, model_name="Model"):
    y_pred = model.predict(x_test)

    print(f"\n===== {model_name} Evaluation =====")
    print("Accuracy :", round(accuracy_score(y_test, y_pred), 4))
    print("Precision:", round(precision_score(y_test, y_pred), 4))
    print("Recall   :", round(recall_score(y_test, y_pred), 4))
    print("F1 Score :", round(f1_score(y_test, y_pred), 4))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


def save_model(model, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as file:
        pickle.dump(model, file)
    print(f"\nModel saved to: {path}")


def main():
    print("Loading dataset...")
    df = load_dataset(DATASET_PATH)
    print(f"Dataset loaded successfully. Total rows: {len(df)}")

    x = df.drop(columns=["label"])
    y = df["label"]

    print("\nFeature sample:")
    print(x.head())

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )
    rf_model.fit(x_train, y_train)
    evaluate_model(rf_model, x_test, y_test, "Random Forest")

    # Logistic Regression
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(x_train, y_train)
    evaluate_model(lr_model, x_test, y_test, "Logistic Regression")

    # Save best model
    best_model = rf_model
    save_model(best_model, MODEL_PATH)

    print("\nTop feature importances from Random Forest:")
    importances = pd.Series(rf_model.feature_importances_, index=x.columns)
    print(importances.sort_values(ascending=False))


if __name__ == "__main__":
    main()