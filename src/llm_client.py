from __future__ import annotations

import json
import os
from typing import Any, Dict

import streamlit as st
from huggingface_hub import InferenceClient


SYSTEM_PROMPT = """You are a cautious AI lending decision support assistant.
You do not make legal claims. You summarize borrower risk, explain major risk drivers,
use retrieved regulatory context carefully, and produce a concise JSON object only.
Avoid hallucinations. If the regulations are generic, say so explicitly.
"""


def get_secret(name: str, default: str = "") -> str:
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, default)


HF_TOKEN = get_secret("HF_TOKEN")
HF_MODEL = get_secret("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")


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


def _fallback_response(payload: Dict[str, Any], extra_note: str = "") -> Dict[str, str]:
    borrower = payload["borrower_profile"]

    reasoning = (
        f"Model probability is {payload['risk_probability']:.2%}, classified as {payload['risk_class']} risk. "
        f"Primary drivers: {'; '.join(payload['key_risk_drivers'])}."
    )

    if extra_note:
        reasoning += f" {extra_note}"

    return {
        "borrower_summary": (
            f"Applicant age {borrower['person_age']} with income "
            f"{borrower['person_income']:.0f} requested a loan of "
            f"{borrower['loan_amnt']:.0f} for {borrower['loan_intent'].lower()}."
        ),
        "reasoning_notes": reasoning,
        "recommendation_summary": (
            f"Recommended action: {payload['recommended_action']}. "
            f"Use retrieved guidance to support a human underwriter decision."
        ),
        "disclaimer": (
            "This tool provides decision support only and must not replace official policy, "
            "regulatory review, or human judgment."
        ),
    }


def generate_reasoning(payload: Dict[str, Any]) -> Dict[str, str]:
    if not HF_TOKEN:
        return _fallback_response(payload, "HF_TOKEN was not found, so fallback reasoning was used.")

    try:
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

        raw = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(raw)

            return {
                "borrower_summary": parsed.get("borrower_summary", ""),
                "reasoning_notes": parsed.get("reasoning_notes", ""),
                "recommendation_summary": parsed.get("recommendation_summary", ""),
                "disclaimer": parsed.get(
                    "disclaimer",
                    "This tool provides decision support only and must not replace official policy, regulatory review, or human judgment.",
                ),
            }
        except Exception:
            return _fallback_response(payload, f"LLM response could not be parsed cleanly. Raw response: {raw[:300]}")

    except Exception as e:
        return _fallback_response(payload, f"Hugging Face inference failed: {str(e)}")