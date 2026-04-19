from __future__ import annotations

import json
from typing import Any, Dict, List

from huggingface_hub import InferenceClient

from src.config import HF_MODEL, HF_TOKEN


SYSTEM_PROMPT = """You are a cautious AI lending decision support assistant.
You do not make legal claims. You summarize borrower risk, explain major risk drivers,
use retrieved regulatory context carefully, and produce a concise JSON object only.
Avoid hallucinations. If the regulations are generic, say so explicitly.
"""


def _build_prompt(payload: Dict[str, Any]) -> str:
    return f"""
Borrower profile:
{json.dumps(payload['borrower_profile'], indent=2)}

Model prediction:
- risk_probability: {payload['risk_probability']}
- risk_class: {payload['risk_class']}
- recommended_action: {payload['recommended_action']}
- key_risk_drivers: {payload['key_risk_drivers']}

Retrieved regulations:
{json.dumps(payload['retrieved_context'], indent=2)}

Return valid JSON with keys:
borrower_summary, reasoning_notes, recommendation_summary, disclaimer
"""


def generate_reasoning(payload: Dict[str, Any]) -> Dict[str, str]:
    if not HF_TOKEN:
        return {
            "borrower_summary": (
                f"Applicant age {payload['borrower_profile']['person_age']} with income "
                f"{payload['borrower_profile']['person_income']:.0f} requested a loan of "
                f"{payload['borrower_profile']['loan_amnt']:.0f} for {payload['borrower_profile']['loan_intent'].lower()}."
            ),
            "reasoning_notes": (
                f"Model probability is {payload['risk_probability']:.2%}, classified as {payload['risk_class']} risk. "
                f"Primary drivers: {'; '.join(payload['key_risk_drivers'])}"
            ),
            "recommendation_summary": (
                f"Recommended action: {payload['recommended_action']}. "
                f"Use retrieved guidance to support a human underwriter decision."
            ),
            "disclaimer": "This tool provides decision support only and must not replace official policy, regulatory review, or human judgment.",
        }

    client = InferenceClient(api_key=HF_TOKEN)
    response = client.chat_completion(
        model=HF_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_prompt(payload)},
        ],
        max_tokens=500,
        temperature=0.2,
    )
    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except Exception:
        return {
            "borrower_summary": "LLM response could not be parsed cleanly; using fallback summary.",
            "reasoning_notes": raw[:500],
            "recommendation_summary": f"Recommended action: {payload['recommended_action']}",
            "disclaimer": "This tool provides decision support only and must not replace official policy, regulatory review, or human judgment.",
        }
