from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)

DATA_URL = "https://raw.githubusercontent.com/PALAK7890/GenAI_Capstone/refs/heads/main/credit_risk_dataset.csv"

GRADE_MAPPING = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
}


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["person_emp_length"] = df["person_emp_length"].fillna(df["person_emp_length"].median())
    df["loan_int_rate"] = df["loan_int_rate"].fillna(df["loan_int_rate"].median())

    df["loan_grade"] = df["loan_grade"].map(GRADE_MAPPING)
    df["cb_person_default_on_file"] = df["cb_person_default_on_file"].map({"Y": 1, "N": 0})

    df = pd.get_dummies(
        df,
        columns=["person_home_ownership", "loan_intent"],
        drop_first=True,
    )

    bool_cols = df.select_dtypes(include="bool").columns
    if len(bool_cols) > 0:
        df[bool_cols] = df[bool_cols].astype(int)

    return df


def train_and_save() -> None:
    df = load_data()
    df = preprocess_data(df)

    X = df.drop("loan_status", axis=1)
    y = df["loan_status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = DecisionTreeClassifier(
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        class_weight="balanced",
        random_state=42,
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)

    print("\nTraining complete")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC-AUC:  {roc_auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, ARTIFACTS_DIR / "decision_tree_model.pkl")
    joblib.dump(list(X.columns), ARTIFACTS_DIR / "feature_columns.pkl")

    print("\nSaved files:")
    print(ARTIFACTS_DIR / "decision_tree_model.pkl")
    print(ARTIFACTS_DIR / "feature_columns.pkl")


if __name__ == "__main__":
    train_and_save()