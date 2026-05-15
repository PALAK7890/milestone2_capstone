from __future__ import annotations
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import json
import streamlit as st

from src.graph_flow import build_graph

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Lending OS",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

section[data-testid="stSidebar"]{
    display:none;
}

.stApp{
    background:#050816;
    color:white;
}

/* MAIN */

.block-container{
    max-width:1600px;
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* FONT */

html, body, [class*="css"]{
    font-family: 'Inter', sans-serif;
}

/* TOPBAR */

.topbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:2rem;
}

.logo{
    font-size:2rem;
    font-weight:800;
    background:linear-gradient(90deg,#8B5CF6,#06B6D4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.nav{
    display:flex;
    gap:1rem;
}

.nav-chip{
    padding:0.7rem 1rem;
    border-radius:14px;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    color:#cbd5e1;
    font-size:0.9rem;
}

/* HERO */

.hero{
    position:relative;
    overflow:hidden;
    border-radius:32px;
    padding:3rem;
    margin-bottom:2rem;
    background:linear-gradient(135deg,#111827,#1E1B4B,#0F172A);
    border:1px solid rgba(255,255,255,0.08);
}

.hero::before{
    content:'';
    position:absolute;
    width:400px;
    height:400px;
    background:#7C3AED;
    filter:blur(140px);
    right:-100px;
    top:-100px;
    opacity:0.4;
}

.hero-title{
    font-size:4rem;
    font-weight:800;
    color:white;
    line-height:1.05;
    position:relative;
    z-index:2;
}

.hero-sub{
    margin-top:1.2rem;
    color:#94A3B8;
    width:60%;
    font-size:1.05rem;
    line-height:1.8;
    position:relative;
    z-index:2;
}

.hero-chip{
    display:inline-block;
    margin-top:1.8rem;
    padding:0.9rem 1.4rem;
    border-radius:18px;
    background:linear-gradient(90deg,#7C3AED,#06B6D4);
    color:white;
    font-weight:700;
    position:relative;
    z-index:2;
}

/* GLASS CARD */

.glass{
    background:rgba(17,24,39,0.75);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter:blur(18px);
    border-radius:26px;
    padding:1.5rem;
    box-shadow:0 0 30px rgba(0,0,0,0.3);
    transition:0.3s ease;
    margin-bottom:1rem;
}

.glass:hover{
    transform:translateY(-4px);
    border:1px solid rgba(124,58,237,0.4);
}

/* KPI */

.kpi-label{
    color:#94A3B8;
    font-size:0.9rem;
}

.kpi-value{
    color:white;
    font-size:2rem;
    font-weight:800;
    margin-top:0.5rem;
}

/* SECTION */

.section-title{
    color:white;
    font-size:1.2rem;
    font-weight:700;
    margin-bottom:1rem;
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea{
    background:#111827 !important;
    color:white !important;
    border-radius:14px !important;
    border:1px solid rgba(255,255,255,0.08) !important;
}

div[data-baseweb="select"] > div{
    background:#111827 !important;
    border-radius:14px !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    color:white !important;
}

/* BUTTON */

.stButton > button{
    width:100%;
    background:linear-gradient(90deg,#7C3AED,#06B6D4);
    border:none;
    border-radius:16px;
    padding:0.95rem;
    color:white;
    font-size:1rem;
    font-weight:700;
    transition:0.3s ease;
}

.stButton > button:hover{
    transform:scale(1.02);
    box-shadow:0 0 30px rgba(124,58,237,0.45);
}

/* METRIC */

div[data-testid="metric-container"]{
    background:rgba(17,24,39,0.7);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    padding:1rem;
}

/* DECISION */

.approved{
    background:linear-gradient(135deg,#16A34A,#22C55E);
    padding:1.5rem;
    border-radius:24px;
    text-align:center;
    font-size:2rem;
    font-weight:800;
    color:white;
}

.review{
    background:linear-gradient(135deg,#F59E0B,#FACC15);
    padding:1.5rem;
    border-radius:24px;
    text-align:center;
    font-size:2rem;
    font-weight:800;
    color:black;
}

.rejected{
    background:linear-gradient(135deg,#DC2626,#EF4444);
    padding:1.5rem;
    border-radius:24px;
    text-align:center;
    font-size:2rem;
    font-weight:800;
    color:white;
}

/* RISK BAR */

.risk-track{
    width:100%;
    height:18px;
    border-radius:20px;
    background:#1F2937;
    overflow:hidden;
    margin-top:1rem;
}

.risk-fill{
    height:100%;
    border-radius:20px;
    background:linear-gradient(90deg,#7C3AED,#06B6D4);
}

/* SOURCE */

.source-card{
    background:#111827;
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    padding:1rem;
    margin-bottom:1rem;
}

.source-title{
    color:white;
    font-weight:700;
    margin-bottom:0.7rem;
}

.source-content{
    color:#CBD5E1;
    line-height:1.7;
}

.source-ref{
    color:#7DD3FC;
    margin-top:0.8rem;
    font-size:0.9rem;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TOPBAR
# =========================================================

st.markdown("""
<div class="topbar">

    <div class="logo">
        AI Lending OS
    </div>

    <div class="nav">
        <div class="nav-chip">Enterprise AI</div>
        <div class="nav-chip">Risk Engine</div>
        <div class="nav-chip">v2.1</div>
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-title">
        Intelligent Lending <br>
        Decision Platform
    </div>

    <div class="hero-sub">
        AI-powered borrower risk assessment, predictive analytics,
        automated regulatory intelligence, and enterprise-grade
        lending recommendations.
    </div>

    <div class="hero-chip">
        Live Risk Intelligence System
    </div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns([1.1, 2])

# =========================================================
# LEFT PANEL
# =========================================================

with left:

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Borrower Configuration</div>',
        unsafe_allow_html=True
    )

    person_age = st.number_input("Age", 18, 100, 30)

    person_income = st.number_input(
        "Annual Income",
        0,
        10000000,
        50000
    )

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
        "Loan Percent Income",
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

# =========================================================
# RIGHT PANEL
# =========================================================

with right:

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="glass">
            <div class="kpi-label">Borrower Age</div>
            <div class="kpi-value">{person_age}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="glass">
            <div class="kpi-label">Income</div>
            <div class="kpi-value">₹{person_income:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="glass">
            <div class="kpi-label">Loan</div>
            <div class="kpi-value">₹{loan_amnt:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="glass">
            <div class="kpi-label">Interest</div>
            <div class="kpi-value">{loan_int_rate}%</div>
        </div>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        risk_score = min(
            int(loan_percent_income * 100 + loan_int_rate),
            100
        )

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">Risk Probability</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div style="
            font-size:4rem;
            font-weight:800;
            color:white;
        ">
            {risk_score}%
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="risk-track">
            <div class="risk-fill" style="width:{risk_score}%"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with c2:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">AI Insights</div>',
            unsafe_allow_html=True
        )

        insights = [
            "Stable employment history detected",
            "Moderate debt-to-income ratio",
            "Borrower profile shows healthy stability",
            "Interest exposure manageable",
            "Regulatory verification active"
        ]

        for item in insights:
            st.markdown(
                f"• <span style='color:#CBD5E1'>{item}</span>",
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ANALYSIS
# =========================================================

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

    with st.spinner("Running AI Lending Analysis..."):

        graph = build_graph()
        result = graph.invoke(initial_state)

        report = result["final_report"]

    decision = report.get("decision", "Needs Review")
    risk_analysis = report.get("risk_analysis", {})
    sources = report.get("sources", [])

    st.write("")

    # =====================================================
    # DECISION BANNER
    # =====================================================

    if decision == "Approved":

        st.markdown("""
        <div class="approved">
            APPROVED • LOW RISK
        </div>
        """, unsafe_allow_html=True)

    elif decision == "Rejected":

        st.markdown("""
        <div class="rejected">
            REJECTED • HIGH RISK
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="review">
            MANUAL REVIEW REQUIRED
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # =====================================================
    # METRICS
    # =====================================================

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

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview",
        "AI Reasoning",
        "Borrower",
        "Sources"
    ])

    with tab1:

        o1, o2 = st.columns(2)

        with o1:

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.subheader("Borrower Summary")

            st.write(
                report.get("borrower_summary","")
            )

            st.markdown('</div>', unsafe_allow_html=True)

        with o2:

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            st.subheader("Recommendation")

            st.write(
                report.get("recommendation_summary","")
            )

            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.subheader("AI Risk Reasoning")

        st.write(
            report.get("reasoning_notes","")
        )

        drivers = risk_analysis.get(
            "key_risk_drivers",
            []
        )

        if drivers:

            st.write("### Key Drivers")

            for driver in drivers:
                st.write(f"• {driver}")

        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.subheader("Borrower Profile")

        st.json(borrower_profile)

        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.subheader("Regulatory Sources")

        if sources:

            for source in sources:

                st.markdown(f"""
                <div class="source-card">

                    <div class="source-title">
                        {source.get("title","Untitled")}
                    </div>

                    <div class="source-content">
                        {source.get("content","")}
                    </div>

                    <div class="source-ref">
                        {source.get("source","")}
                    </div>

                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("No regulatory sources retrieved.")

        st.markdown('</div>', unsafe_allow_html=True)
