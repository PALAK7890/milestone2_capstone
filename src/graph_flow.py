from __future__ import annotations

from langgraph.graph import END, StateGraph

from src.model_utils import predict_credit_risk
from src.rag import retrieve_regulations
from src.reasoning import generate_reasoning
from src.report import build_final_report
from src.schemas import AgentState


def predict_node(state: AgentState) -> AgentState:
    result = predict_credit_risk(state["borrower_profile"])

    return {
        "feature_row": result["feature_row"],
        "prediction": result["prediction"],
        "risk_probability": result["risk_probability"],
        "risk_class": result["risk_class"],
        "recommended_action": result["recommended_action"],
        "key_risk_drivers": result["key_risk_drivers"],
    }


def retrieval_node(state: AgentState) -> AgentState:
    contexts = retrieve_regulations(
        lending_query=state.get("lending_query", ""),
        borrower_profile=state["borrower_profile"],
        risk_class=state.get("risk_class", "Unknown"),
        recommended_action=state.get("recommended_action", "Needs Review"),
        top_k=3,
    )
    return {"retrieved_context": contexts}


def reason_node(state: AgentState) -> AgentState:
    reasoning = generate_reasoning(state)

    return {
        "borrower_summary": reasoning.get("borrower_summary", ""),
        "reasoning_notes": reasoning.get("reasoning_notes", ""),
        "recommendation_summary": reasoning.get("recommendation_summary", ""),
        "disclaimer": reasoning.get(
            "disclaimer",
            "This tool provides decision support only and must not replace human judgment."
        ),
    }


def report_node(state: AgentState) -> AgentState:
    return {"final_report": build_final_report(state)}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("predict", predict_node)
    graph.add_node("retrieve", retrieval_node)
    graph.add_node("reason", reason_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("predict")
    graph.add_edge("predict", "retrieve")
    graph.add_edge("retrieve", "reason")
    graph.add_edge("reason", "report")
    graph.add_edge("report", END)

    return graph.compile()