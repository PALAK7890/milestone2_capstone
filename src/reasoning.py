from __future__ import annotations

from typing import Any, Dict, List


def _format_sources(sources: List[Dict[str, str]]) -> str:
    if not sources:
        return "No specific regulation retrieved."

    titles = [src.get("title", "Untitled") for src in sources]
    return ", ".join(titles)


def generate_reasoning(state: Dict[str, Any]) -> Dict[str, str]:
    borrower = state.get("borrower_profile", {})
    risk_probability = state.get("risk_probability", 0.0)
    risk_class = state.get("risk_class", "Unknown")
    recommended_action = state.get("recommended_action", "Needs Review")
    key_risk_drivers = state.get("key_risk_drivers", [])
    retrieved_context = state.get("retrieved_context", [])

    borrower_summary = (
        f"Applicant age {borrower.get('person_age', 'N/A')} with annual income "
        f"{borrower.get('person_income', 'N/A')} requested a loan of "
        f"{borrower.get('loan_amnt', 'N/A')} for "
        f"{str(borrower.get('loan_intent', 'unknown')).lower()}."
    )

    drivers_text = (
        ", ".join(key_risk_drivers)
        if key_risk_drivers
        else "No major drivers identified"
    )

    source_text = _format_sources(retrieved_context)

    reasoning_notes = (
        f"The borrower is classified as {risk_class} risk with an estimated default "
        f"probability of {risk_probability:.2%}. "
        f"Important risk drivers include: {drivers_text}. "
        f"Relevant regulatory references were retrieved from: {source_text}."
    )

    recommendation_summary = (
        f"Recommended lending action: {recommended_action}. "
        f"This recommendation is based on the borrower profile, predicted risk, "
        f"and retrieved regulatory guidance."
    )

    disclaimer = (
        "This system is a decision-support assistant for academic and demo purposes. "
        "It should not be used as the sole basis for lending approval, rejection, "
        "or legal/regulatory compliance decisions."
    )

    return {
        "borrower_summary": borrower_summary,
        "reasoning_notes": reasoning_notes,
        "recommendation_summary": recommendation_summary,
        "disclaimer": disclaimer,
    }