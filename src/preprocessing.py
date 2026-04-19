from __future__ import annotations

from typing import Dict, Any
import pandas as pd

GRADE_MAPPING = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}
DEFAULT_MAPPING = {"Y": 1, "N": 0}

BASE_COLUMNS = [
    "person_age",
    "person_income",
    "person_home_ownership",
    "person_emp_length",
    "loan_intent",
    "loan_grade",
    "loan_amnt",
    "loan_int_rate",
    "loan_percent_income",
    "cb_person_default_on_file",
    "cb_person_cred_hist_length",
]


def preprocess_training_data(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["person_emp_length"] = data["person_emp_length"].fillna(data["person_emp_length"].median())
    data["loan_int_rate"] = data["loan_int_rate"].fillna(data["loan_int_rate"].median())

    data["loan_grade"] = data["loan_grade"].map(GRADE_MAPPING)
    data["cb_person_default_on_file"] = data["cb_person_default_on_file"].map(DEFAULT_MAPPING)

    data = pd.get_dummies(
        data,
        columns=["person_home_ownership", "loan_intent"],
        drop_first=True,
    )

    bool_cols = data.select_dtypes(include="bool").columns
    if len(bool_cols) > 0:
        data[bool_cols] = data[bool_cols].astype(int)
    return data


def build_feature_row(borrower_profile: Dict[str, Any], feature_columns: list[str]) -> pd.DataFrame:
    raw = pd.DataFrame([{k: borrower_profile[k] for k in BASE_COLUMNS if k in borrower_profile}])
    raw["loan_grade"] = raw["loan_grade"].map(GRADE_MAPPING)
    raw["cb_person_default_on_file"] = raw["cb_person_default_on_file"].map(DEFAULT_MAPPING)

    encoded = pd.get_dummies(
        raw,
        columns=["person_home_ownership", "loan_intent"],
        drop_first=True,
    )

    for col in feature_columns:
        if col not in encoded.columns:
            encoded[col] = 0

    encoded = encoded[feature_columns]
    return encoded
