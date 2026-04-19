from __future__ import annotations
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"


import json
import streamlit as st

from src.graph_flow import build_graph

st.set_page_config(
    page_title="AI Lending Decision Support",
    page_icon="💳",
    layout="wide",
)

# ---------- Custom Styling ----------
st.markdown(
    """
    <style>
        .main {
            background-color: #f7f9fc;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1250px;
        }

        .title-text {
            font-size: 2.2rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.2rem;
        }

        .subtitle-text {
            font-size: 1rem;
            color: #475569;
            margin-bottom: 1.5rem;
        }

        .section-card {
            background: white;
            padding: 1.2rem 1.2rem;
            border-radius: 16px;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
            border: 1px solid #e2e8f0;
        }

        .decision-approved {
            padding: 1rem 1.2rem;
            border-radius: 14px;
            background: #dcfce7;
            color: #166534;
            font-weight: 700;
            font-size: 1.1rem;
            border: 1px solid #86efac;
            text-align: center;
        }

        .decision-review {
            padding: 1rem 1.2rem;
            border-radius: 14px;
            background: #fef3c7;
            color: #92400e;
            font-weight: 700;
            font-size: 1.1rem;
            border: 1px solid #fcd34d;
            text-align: center;
        }

        .decision-rejected {
            padding: 1rem 1.2rem;
            border-radius: 14px;
            background: #fee2e2;
            color: #991b1b;
            font-weight: 700;
            font-size: 1.1rem;
            border: 1px solid #fca5a5;
            text-align: center;
        }

        .mini-label {
            font-size: 0.9rem;
            color: #64748b;
            margin-bottom: 0.3rem;
            font-weight: 600;
        }

        .source-box {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.9rem;
            margin-bottom: 0.8rem;
        }

        .json-box {
            background: #0f172a;
            color: #e2e8f0;
            border-radius: 12px;
            padding: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown('<div class="title-text">AI Lending Decision Support Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-text">Credit risk prediction, regulation retrieval, and structured lending recommendations</div>',
    unsafe_allow_html=True,
)

# ---------- Sidebar Input ----------
st.sidebar.header("Borrower Input")
st.sidebar.markdown("Enter the borrower profile and run the assessment.")

person_age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)
person_income = st.sidebar.number_input("Annual Income", min_value=0, value=50000)
person_home_ownership = st.sidebar.selectbox(
    "Home Ownership",
    ["RENT", "OWN", "MORTGAGE", "OTHER"]
)

person_emp_length = st.sidebar.number_input(
    "Employment Length (years)", min_value=0.0, max_value=60.0, value=5.0
)

loan_intent = st.sidebar.selectbox(
    "Loan Purpose",
    ["EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"]
)

loan_grade = st.sidebar.selectbox(
    "Loan Grade",
    ["A", "B", "C", "D", "E", "F", "G"]
)

loan_amnt = st.sidebar.number_input("Loan Amount", min_value=0, value=15000)
loan_int_rate = st.sidebar.number_input(
    "Interest Rate (%)", min_value=0.0, max_value=100.0, value=12.5
)
loan_percent_income = st.sidebar.number_input(
    "Loan Percent of Income", min_value=0.0, max_value=1.0, value=0.30
)

cb_person_default_on_file = st.sidebar.selectbox(
    "Previous Default on File",
    ["N", "Y"]
)

cb_person_cred_hist_length = st.sidebar.number_input(
    "Credit History Length", min_value=0, max_value=50, value=6
)

lending_query = st.sidebar.text_area(
    "Lending Query",
    value="Should this borrower be approved for a personal loan?"
)

run_btn = st.sidebar.button("Analyze Borrower", use_container_width=True)

# ---------- Top Dashboard Preview ----------
top1, top2, top3, top4 = st.columns(4)

with top1:
    st.markdown('<div class="section-card"><div class="mini-label">Borrower Age</div><h3>{}</h3></div>'.format(person_age), unsafe_allow_html=True)

with top2:
    st.markdown('<div class="section-card"><div class="mini-label">Income</div><h3>₹{:,.0f}</h3></div>'.format(person_income), unsafe_allow_html=True)

with top3:
    st.markdown('<div class="section-card"><div class="mini-label">Loan Amount</div><h3>₹{:,.0f}</h3></div>'.format(loan_amnt), unsafe_allow_html=True)

with top4:
    st.markdown('<div class="section-card"><div class="mini-label">Interest Rate</div><h3>{:.2f}%</h3></div>'.format(loan_int_rate), unsafe_allow_html=True)

# ---------- Main Processing ----------
if run_btn:
    borrower_profile = {
        "person_age": int(person_age),
        "person_income": int(person_income),
        "person_home_ownership": person_home_ownership,
        "person_emp_length": float(person_emp_length),
        "loan_intent": loan_intent,
        "loan_grade": loan_grade,
        "loan_amnt": int(loan_amnt),
        "loan_int_rate": float(loan_int_rate),
        "loan_percent_income": float(loan_percent_income),
        "cb_person_default_on_file": cb_person_default_on_file,
        "cb_person_cred_hist_length": int(cb_person_cred_hist_length),
    }

    initial_state = {
        "borrower_profile": borrower_profile,
        "lending_query": lending_query,
    }

    with st.spinner("Running credit risk assessment..."):
        graph = build_graph()
        result = graph.invoke(initial_state)
        report = result["final_report"]

    decision = report.get("decision", "Needs Review")
    risk_analysis = report.get("risk_analysis", {})
    sources = report.get("sources", [])

    # ---------- Decision Banner ----------
    if decision == "Approved":
        st.markdown(f'<div class="decision-approved">✅ Final Recommendation: {decision}</div>', unsafe_allow_html=True)
    elif decision == "Rejected":
        st.markdown(f'<div class="decision-rejected">❌ Final Recommendation: {decision}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="decision-review">⚠️ Final Recommendation: {decision}</div>', unsafe_allow_html=True)

    st.write("")

    # ---------- Risk Metrics ----------
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Risk Probability", f"{risk_analysis.get('risk_probability', 0.0):.2%}")
    with m2:
        st.metric("Risk Class", risk_analysis.get("risk_class", "Unknown"))
    with m3:
        st.metric("Predicted Class", str(risk_analysis.get("prediction", 0)))

    # ---------- Main Content ----------
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Borrower Summary")
        st.write(report.get("borrower_summary", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Risk Reasoning")
        st.write(report.get("reasoning_notes", ""))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Recommendation Summary")
        st.write(report.get("recommendation_summary", ""))
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Key Risk Drivers")
        drivers = risk_analysis.get("key_risk_drivers", [])
        if drivers:
            for driver in drivers:
                st.write(f"• {driver}")
        else:
            st.write("No major drivers identified.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Borrower Profile Snapshot")
        st.json(borrower_profile)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Sources ----------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Regulatory Sources")
    if sources:
        for idx, source in enumerate(sources, start=1):
            st.markdown(f"""
            <div class="source-box">
                <b>Source {idx}: {source.get("title", "Untitled")}</b><br><br>
                {source.get("content", "")}<br><br>
                <i>Reference: {source.get("source", "")}</i>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No regulatory sources retrieved.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Disclaimer ----------
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Disclaimer")
    st.warning(report.get("disclaimer", ""))
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Expandable JSON ----------
    with st.expander("View Full Structured Report (JSON)"):
        st.code(json.dumps(report, indent=2), language="json")

else:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("How this works")
    st.write(
        """
        This lending assistant:
        - predicts borrower credit risk,
        - explains the important risk drivers,
        - retrieves regulatory guidance using RAG,
        - and generates a structured lending recommendation.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)