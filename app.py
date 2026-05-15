from __future__ import annotations
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import json
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from src.graph_flow import build_graph

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Lending OS",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# REMOVE SIDEBAR + GLOBAL STYLING
# ---------------------------------------------------

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

section[data-testid="stSidebar"]{
    display: none;
}

.stApp{
    background: #070B14;
    color: white;
    overflow-x: hidden;
}

/* ---------- GLOBAL ---------- */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---------- MAIN CONTAINER ---------- */

.block-container{
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1600px;
}

/* ---------- TOP NAV ---------- */

.topbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:2rem;
}

.logo{
    font-size:1.7rem;
    font-weight:800;
    background: linear-gradient(90deg,#7C3AED,#06B6D4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.nav-right{
    display:flex;
    gap:1rem;
    align-items:center;
}

.nav-chip{
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    padding:0.6rem 1rem;
    border-radius:12px;
    color:#cbd5e1;
    font-size:0.9rem;
}

/* ---------- HERO ---------- */

.hero{
    background: linear-gradient(135deg,#1e1b4b,#111827,#0f172a);
    border-radius:28px;
    padding:2rem;
    margin-bottom:2rem;
    border:1px solid rgba(255,255,255,0.08);
    position:relative;
    overflow:hidden;
}

.hero::before{
    content:'';
    position:absolute;
    width:300px;
    height:300px;
    background:#7c3aed;
    filter:blur(120px);
    top:-100px;
    right:-100px;
    opacity:0.35;
}

.hero-title{
    font-size:3rem;
    font-weight:800;
    line-height:1.1;
    color:white;
}

.hero-sub{
    color:#94a3b8;
    margin-top:1rem;
    font-size:1rem;
    width:60%;
}

.hero-badge{
    margin-top:1.5rem;
    display:inline-block;
    background:linear-gradient(90deg,#7c3aed,#06b6d4);
    padding:0.7rem 1.2rem;
    border-radius:14px;
    font-weight:600;
    color:white;
}

/* ---------- GLASS CARDS ---------- */

.glass-card{
    background: rgba(17,24,39,0.7);
    backdrop-filter: blur(18px);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:24px;
    padding:1.4rem;
    box-shadow: 0 0 30px rgba(0,0,0,0.25);
    transition:0.3s ease;
}

.glass-card:hover{
    transform:translateY(-4px);
    border:1px solid rgba(124,58,237,0.5);
}

/* ---------- KPI ---------- */

.kpi-label{
    color:#94a3b8;
    font-size:0.9rem;
    margin-bottom:0.5rem;
}

.kpi-value{
    font-size:2rem;
    font-weight:800;
    color:white;
}

/* ---------- SECTION ---------- */

.section-title{
    font-size:1.2rem;
    font-weight:700;
    margin-bottom:1rem;
    color:white;
}

/* ---------- INPUTS ---------- */

.stNumberInput,
.stSelectbox,
.stTextArea{
    background: transparent !important;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea{
    background:#111827 !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:14px !important;
    color:white !important;
}

div[data-baseweb="select"] > div{
    background:#111827 !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:14px !important;
    color:white !important;
}

/* ---------- BUTTON ---------- */

.stButton > button{
    width:100%;
    background:linear-gradient(90deg,#7c3aed,#06b6d4);
    color:white;
    border:none;
    border-radius:16px;
    padding:0.9rem;
    font-weight:700;
    font-size:1rem;
    transition:0.3s ease;
}

.stButton > button:hover{
    transform:scale(1.02);
    box-shadow:0 0 25px rgba(124,58,237,0.5);
}

/* ---------- METRICS ---------- */

div[data-testid="metric-container"]{
    background: rgba(17,24,39,0.7);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    padding:1rem;
}

/* ---------- DECISION ---------- */

.approved{
    background: linear-gradient(135deg,#16a34a,#22c55e);
    padding:1.5rem;
    border-radius:24px;
    font-size:2rem;
    font-weight:800;
    color:white;
    text-align:center;
}

.review{
    background: linear-gradient(135deg,#f59e0b,#facc15);
    padding:1.5rem;
    border-radius:24px;
    font-size:2rem;
    font-weight:800;
    color:black;
    text-align:center;
}

.rejected{
    background: linear-gradient(135deg,#dc2626,#ef4444);
    padding:1.5rem;
    border-radius:24px;
    font-size:2rem;
    font-weight:800;
    color:white;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TOPBAR
# ---------------------------------------------------

st.markdown("""
<div class="topbar">
    <div class="logo">AI Lending OS</div>

    <div class="nav-right">
        <div class="nav-chip">Enterprise AI</div>
        <div class="nav-chip">Risk Intelligence</div>
        <div class="nav-chip">v2.1</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        AI Powered <br>
        Lending Decision Platform
    </div>

    <div class="hero-sub">
        Advanced borrower risk assessment, intelligent lending recommendations,
        AI-driven regulatory retrieval, and enterprise-grade analytics.
    </div>

    <div class="hero-badge">
        Live Risk Intelligence System
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# INPUT + KPI ROW
# ---------------------------------------------------

left, right = st.columns([1.1, 2])

# ---------------------------------------------------
# LEFT PANEL
# ---------------------------------------------------

with left:

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Borrower Configuration</div>',
        unsafe_allow_html=True
    )

    person_age = st.number_input("Age", 18, 100, 30)
    person_income = st.number_input("Annual Income", 0, 10000000, 50000)

    person_home_ownership = st.selectbox(
        "Home Ownership",
        ["RENT", "OWN", "MORTGAGE", "OTHER"]
    )

    person_emp_length = st.number_input(
        "Employment Length",
        0.0,
        50.0,
        5.0
    )

    loan_intent = st.selectbox(
        "Loan Purpose",
        [
            "EDUCATION",
            "MEDICAL",
            "VENTURE",
            "PERSONAL",
            "HOMEIMPROVEMENT",
            "DEBTCONSOLIDATION"
        ]
    )

    loan_grade = st.selectbox(
        "Loan Grade",
        ["A","B","C","D","E","F","G"]
    )

    loan_amnt = st.number_input(
        "Loan Amount",
        0,
        1000000,
        15000
    )

    loan_int_rate = st.number_input(
        "Interest Rate",
        0.0,
        100.0,
        12.5
    )

    loan_percent_income = st.number_input(
        "Loan % Income",
        0.0,
        1.0,
        0.30
    )

    cb_person_default_on_file = st.selectbox(
        "Previous Default",
        ["N","Y"]
    )

    cb_person_cred_hist_length = st.number_input(
        "Credit History Length",
        0,
        50,
        6
    )

    lending_query = st.text_area(
        "Lending Query",
        "Should this borrower be approved?"
    )

    run_btn = st.button("Analyze Borrower")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# RIGHT PANEL
# ---------------------------------------------------

with right:

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-label">Age</div>
            <div class="kpi-value">{person_age}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-label">Income</div>
            <div class="kpi-value">₹{person_income:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-label">Loan</div>
            <div class="kpi-value">₹{loan_amnt:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-label">Interest</div>
            <div class="kpi-value">{loan_int_rate}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ---------------------------------------------------
    # CHARTS PLACEHOLDER
    # ---------------------------------------------------

    chart1, chart2 = st.columns(2)

    with chart1:

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=72,
            title={'text': "Risk Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#7C3AED"},
                'steps': [
                    {'range': [0, 40], 'color': "#22C55E"},
                    {'range': [40, 75], 'color': "#F59E0B"},
                    {'range': [75, 100], 'color': "#EF4444"},
                ]
            }
        ))

        fig.update_layout(
            paper_bgcolor="#111827",
            font=dict(color="white"),
            height=320
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart2:

        radar = go.Figure()

        radar.add_trace(go.Scatterpolar(
            r=[80, 65, 72, 60, 78],
            theta=[
                'Income',
                'Credit',
                'Employment',
                'Debt',
                'Stability'
            ],
            fill='toself'
        ))

        radar.update_layout(
            polar=dict(
                bgcolor="#111827",
                radialaxis=dict(
                    visible=True,
                    range=[0,100]
                )
            ),
            paper_bgcolor="#111827",
            font=dict(color="white"),
            height=320
        )

        st.plotly_chart(radar, use_container_width=True)

# ---------------------------------------------------
# PROCESSING
# ---------------------------------------------------

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

    with st.spinner("Running AI Risk Analysis..."):

        graph = build_graph()
        result = graph.invoke(initial_state)

        report = result["final_report"]

    decision = report.get("decision", "Needs Review")
    risk_analysis = report.get("risk_analysis", {})
    sources = report.get("sources", [])

    st.write("")

    # ---------------------------------------------------
    # DECISION BANNER
    # ---------------------------------------------------

    if decision == "Approved":
        st.markdown(
            '<div class="approved">APPROVED • LOW RISK</div>',
            unsafe_allow_html=True
        )

    elif decision == "Rejected":
        st.markdown(
            '<div class="rejected">REJECTED • HIGH RISK</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            '<div class="review">MANUAL REVIEW REQUIRED</div>',
            unsafe_allow_html=True
        )

    st.write("")

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Risk Probability",
            f"{risk_analysis.get('risk_probability',0):.2%}"
        )

    with m2:
        st.metric(
            "Risk Class",
            risk_analysis.get("risk_class","Unknown")
        )

    with m3:
        st.metric(
            "Prediction",
            str(risk_analysis.get("prediction",0))
        )

    st.write("")

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview",
        "AI Reasoning",
        "Borrower",
        "Sources"
    ])

    with tab1:

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Borrower Summary")
            st.write(report.get("borrower_summary",""))
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Recommendation")
            st.write(report.get("recommendation_summary",""))
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.subheader("AI Risk Reasoning")

        st.write(report.get("reasoning_notes",""))

        drivers = risk_analysis.get("key_risk_drivers", [])

        if drivers:

            st.write("### Key Drivers")

            for driver in drivers:
                st.write(f"• {driver}")

        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.subheader("Borrower Profile")

        st.json(borrower_profile)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.subheader("Regulatory Sources")

        if sources:

            for source in sources:

                st.markdown(f"""
                <div style="
                    background:#111827;
                    border-radius:18px;
                    padding:1rem;
                    margin-bottom:1rem;
                    border:1px solid rgba(255,255,255,0.08);
                ">
                    <h4 style="color:white;">
                        {source.get("title","Untitled")}
                    </h4>

                    <p style="color:#cbd5e1;">
                        {source.get("content","")}
                    </p>

                    <p style="color:#7dd3fc;">
                        {source.get("source","")}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("No regulatory sources retrieved.")

        st.markdown('</div>', unsafe_allow_html=True)
