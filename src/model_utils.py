from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "decision_tree_model.pkl"
FEATURES_PATH = ARTIFACTS_DIR / "feature_columns.pkl"

GRADE_MAPPING = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
}


def _load_artifacts():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. Run: python3 -m src.train_model"
        )
    if not FEATURES_PATH.exists():
        raise FileNotFoundError(
            f"Feature columns file not found at {FEATURES_PATH}. Run: python3 -m src.train_model"
        )

    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
    return model, feature_columns


def _build_feature_row(
    borrower_profile: Dict[str, Any], feature_columns: List[str]
) -> pd.DataFrame:
    row = {
        "person_age": borrower_profile["person_age"],
        "person_income": borrower_profile["person_income"],
        "person_emp_length": borrower_profile["person_emp_length"],
        "loan_grade": GRADE_MAPPING[borrower_profile["loan_grade"]],
        "loan_amnt": borrower_profile["loan_amnt"],
        "loan_int_rate": borrower_profile["loan_int_rate"],
        "loan_percent_income": borrower_profile["loan_percent_income"],
        "cb_person_default_on_file": 1
        if borrower_profile["cb_person_default_on_file"] == "Y"
        else 0,
        "cb_person_cred_hist_length": borrower_profile["cb_person_cred_hist_length"],
    }

    home_col = f"person_home_ownership_{borrower_profile['person_home_ownership']}"
    intent_col = f"loan_intent_{borrower_profile['loan_intent']}"

    if home_col in feature_columns:
        row[home_col] = 1
    if intent_col in feature_columns:
        row[intent_col] = 1

    df = pd.DataFrame([row])

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]
    return df


def _risk_class(prob: float) -> str:
    if prob < 0.20:
        return "Low"
    if prob < 0.50:
        return "Medium"
    return "High"


def _recommended_action(prob: float) -> str:
    if prob < 0.20:
        return "Approved"
    if prob < 0.50:
        return "Needs Review"
    return "Rejected"


def _pretty_feature_name(name: str) -> str:
    return (
        name.replace("_", " ")
        .replace("cb person", "credit bureau person")
        .replace("loan amnt", "loan amount")
        .replace("loan int rate", "loan interest rate")
        .replace("loan percent income", "loan percent of income")
        .title()
    )


def _top_risk_drivers(model, feature_row: pd.DataFrame, top_n: int = 5) -> List[str]:
    if not hasattr(model, "feature_importances_"):
        return ["Feature importance not available"]

    importance_map = dict(zip(feature_row.columns, model.feature_importances_))
    sorted_features = sorted(
        importance_map.items(), key=lambda x: x[1], reverse=True
    )

    drivers = []
    for feature, importance in sorted_features[:top_n]:
        if importance > 0:
            value = feature_row.iloc[0][feature]
            drivers.append(
                f"{_pretty_feature_name(feature)} = {value} (importance: {importance:.3f})"
            )

    return drivers if drivers else ["No major drivers identified"]


def predict_credit_risk(borrower_profile: Dict[str, Any]) -> Dict[str, Any]:
    model, feature_columns = _load_artifacts()
    feature_df = _build_feature_row(borrower_profile, feature_columns)

    prediction = int(model.predict(feature_df)[0])
    probability = float(model.predict_proba(feature_df)[0][1])

    return {
        "feature_row": feature_df.iloc[0].to_dict(),
        "prediction": prediction,
        "risk_probability": probability,
        "risk_class": _risk_class(probability),
        "recommended_action": _recommended_action(probability),
        "key_risk_drivers": _top_risk_drivers(model, feature_df),
    }