from __future__ import annotations

from typing import Any, Dict, List


def classify_risk(probability: float) -> str:
    if probability < 0.20:
        return "Low"
    if probability < 0.50:
        return "Medium"
    return "High"


def recommended_action(probability: float) -> str:
    if probability < 0.20:
        return "Approved"
    if probability < 0.50:
        return "Needs Review"
    return "Rejected"


def explain_key_drivers(profile: Dict[str, Any], global_importance: Dict[str, float]) -> List[str]:
    drivers: List[str] = []

    if profile["loan_percent_income"] >= 0.35:
        drivers.append("High loan-to-income burden increases repayment stress.")
    elif profile["loan_percent_income"] >= 0.25:
        drivers.append("Moderate loan-to-income burden needs affordability review.")

    if profile["loan_int_rate"] >= 16:
        drivers.append("Higher interest rate is associated with riskier borrowing profiles.")
    elif profile["loan_int_rate"] >= 12:
        drivers.append("Mid-range interest rate adds some repayment pressure.")

    if profile["cb_person_default_on_file"] == "Y":
        drivers.append("Previous default history is a major adverse signal.")

    if profile["loan_grade"] in ["E", "F", "G"]:
        drivers.append("Weak loan grade indicates elevated underwriting risk.")
    elif profile["loan_grade"] in ["C", "D"]:
        drivers.append("Mid-tier loan grade suggests moderate credit quality.")

    if profile["cb_person_cred_hist_length"] <= 3:
        drivers.append("Short credit history reduces confidence in long-term repayment behavior.")

    if profile["person_income"] < 30000:
        drivers.append("Lower income can reduce repayment flexibility.")

    if profile["person_emp_length"] < 2:
        drivers.append("Short employment tenure may indicate unstable income continuity.")

    if not drivers:
        top_global = list(global_importance.keys())[:3]
        readable = [x.replace("_", " ") for x in top_global]
        drivers = [f"Model relied mostly on: {', '.join(readable)}."]

    return drivers[:4]
