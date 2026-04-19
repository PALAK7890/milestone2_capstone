from typing import Any, Dict, List, Literal, Optional, TypedDict
from pydantic import BaseModel, Field


class BorrowerInput(BaseModel):
    person_age: int = Field(..., ge=18, le=100)
    person_income: float = Field(..., gt=0)
    person_home_ownership: Literal["MORTGAGE", "OWN", "RENT", "OTHER"]
    person_emp_length: float = Field(..., ge=0, le=80)
    loan_intent: Literal[
        "EDUCATION",
        "HOMEIMPROVEMENT",
        "MEDICAL",
        "PERSONAL",
        "VENTURE",
        "DEBTCONSOLIDATION",
    ]
    loan_grade: Literal["A", "B", "C", "D", "E", "F", "G"]
    loan_amnt: float = Field(..., gt=0)
    loan_int_rate: float = Field(..., gt=0, le=100)
    loan_percent_income: float = Field(..., gt=0, le=1)
    cb_person_default_on_file: Literal["Y", "N"]
    cb_person_cred_hist_length: int = Field(..., ge=0, le=60)
    lending_query: str = Field(default="Assess this borrower for loan approval.")


class RiskAssessment(BaseModel):
    risk_probability: float
    risk_class: Literal["Low", "Medium", "High"]
    recommended_action: Literal["Approved", "Needs Review", "Rejected"]
    key_risk_drivers: List[str]
    borrower_summary: str
    regulation_sources: List[Dict[str, str]]
    disclaimer: str


class AgentState(TypedDict, total=False):
    borrower_profile: Dict[str, Any]
    lending_query: str

    feature_row: Dict[str, Any]

    prediction: int
    risk_probability: float
    risk_class: str
    recommended_action: str
    key_risk_drivers: List[str]

    retrieved_context: List[Dict[str, str]]

    borrower_summary: str
    reasoning_notes: str
    recommendation_summary: str
    disclaimer: str

    final_report: Dict[str, Any]