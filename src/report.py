from __future__ import annotations

from typing import Any, Dict


def build_final_report(state: Dict[str, Any]) -> Dict[str, Any]:
    borrower = state.get("borrower_profile", {})

    borrower_summary = state.get(
        "borrower_summary",
        (
            f"Applicant age {borrower.get('person_age', 'N/A')} with income "
            f"{borrower.get('person_income', 'N/A')} requested a loan of "
            f"{borrower.get('loan_amnt', 'N/A')} for "
            f"{str(borrower.get('loan_intent', 'unknown')).lower()}."
        ),
    )

    reasoning_notes = state.get(
        "reasoning_notes",
        f"Risk classified as {state.get('risk_class', 'Unknown')} with probability "
        f"{state.get('risk_probability', 0):.2%}.",
    )

    recommendation_summary = state.get(
        "recommendation_summary",
        f"Recommended action: {state.get('recommended_action', 'Needs Review')}.",
    )

    disclaimer = state.get(
        "disclaimer",
        "This tool provides decision support only and must not replace official policy, regulatory review, or human judgment.",
    )

    return {
        "borrower_summary": borrower_summary,
        "risk_analysis": {
            "risk_probability": round(state.get("risk_probability", 0.0), 4),
            "risk_class": state.get("risk_class", "Unknown"),
            "prediction": int(state.get("prediction", 0)),
            "key_risk_drivers": state.get("key_risk_drivers", []),
        },
        "decision": state.get("recommended_action", "Needs Review"),
        "reasoning_notes": reasoning_notes,
        "recommendation_summary": recommendation_summary,
        "sources": state.get("retrieved_context", []),
        "disclaimer": disclaimer,
    }