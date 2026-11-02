"""
PhishGuard - AI-Powered Phishing Email Detection & DSA Visualization System
College Data Structures and Algorithms Mini Project
Next-Gen Cyber Threat Intelligence UI
"""

import html
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="PhishGuard | AI Phishing Shield & DSA Visualizer",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Core imports
from config import CATEGORIES, DEFAULT_SUSPICIOUS_INDICATORS, MODEL_METRICS_PATH
from src.dataset_loader import load_raw_dataset
from src.dsa.binary_search import binary_search_with_trace, prepare_sorted_index_by_id
from src.dsa.hash_table import SeparateChainingHashTable
from src.dsa.linked_list import AnalysisNode, SinglyLinkedList
from src.dsa.merge_sort import merge_sort_analyses, merge_sort_with_trace
from src.dsa.queue import LinkedQueue
from src.dsa.trie import SuspiciousPhraseTrie
from src.model_inference import predict_email
from src.risk_engine import RiskEngine

# -------------------------------------------------------------
# PHENOMENAL CYBERSECURITY & GLASSMORPHISM STYLING
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Dark Theme */
    .stApp {
        background-color: #070B14;
        background-image: 
            radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(129, 140, 248, 0.06) 0px, transparent 50%);
        color: #E2E8F0;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.7) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 18px;
        padding: 26px 32px;
        margin-bottom: 24px;
        box-shadow: 0 12px 36px -4px rgba(0, 0, 0, 0.5), 0 0 24px rgba(56, 189, 248, 0.12);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.0rem;
        font-weight: 500;
        margin-top: 6px;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Cyber Glass Cards */
    .cyber-card {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(51, 65, 85, 0.6);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        transition: all 0.25s ease;
    }
    .cyber-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 8px 30px rgba(56, 189, 248, 0.1);
    }
    .card-heading {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid rgba(51, 65, 85, 0.5);
        padding-bottom: 10px;
    }

    /* Metric Tiles */
    .metric-tile {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.5) 100%);
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    .metric-number {
        font-size: 2.1rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.03em;
    }
    .metric-title {
        font-size: 0.8rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Cyber Verdict Badges */
    .verdict-box-phish {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.18) 0%, rgba(185, 28, 28, 0.08) 100%);
        border: 2px solid #EF4444;
        border-radius: 14px;
        padding: 22px 24px;
        color: #FECACA;
        box-shadow: 0 0 28px rgba(239, 68, 68, 0.25);
        margin-bottom: 22px;
    }
    .verdict-box-legit {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.08) 100%);
        border: 2px solid #10B981;
        border-radius: 14px;
        padding: 22px 24px;
        color: #A7F3D0;
        box-shadow: 0 0 28px rgba(16, 185, 129, 0.25);
        margin-bottom: 22px;
    }
    .verdict-title {
        font-size: 1.45rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        gap: 12px;
        letter-spacing: -0.01em;
    }
    .verdict-desc {
        font-size: 0.95rem;
        margin-top: 6px;
        opacity: 0.9;
    }

    /* Keyword Tags */
    .indicator-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(239, 68, 68, 0.2);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #FCA5A5;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        margin: 4px;
    }

    /* DSA Interactive Visualization Blocks */
    .dsa-node-box {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1.5px solid #38BDF8;
        border-radius: 10px;
        padding: 12px 16px;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
        display: inline-block;
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.2);
        margin: 6px;
    }
    .dsa-arrow {
        color: #38BDF8;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0 6px;
        vertical-align: middle;
        font-family: 'JetBrains Mono', monospace;
    }
    .bucket-card {
        background: #0F172A;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        font-family: 'JetBrains Mono', monospace;
    }
    .bucket-occupied {
        border-color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
    }
    .bucket-collision {
        border-color: #F59E0B;
        background: rgba(245, 158, 11, 0.08);
    }

    /* Streamlit Tab Custom Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(51, 65, 85, 0.5);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #94A3B8;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%) !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# Initialize session state (stores our custom data structures)
# -------------------------------------------------------------
if "risk_engine" not in st.session_state:
    st.session_state.risk_engine = RiskEngine()

if "history_list" not in st.session_state:
    ll = SinglyLinkedList()
    sample_1 = st.session_state.risk_engine.analyze_email(
        "Dear client, we need you to update your billing information. Click here to proceed.",
        analysis_id="EMAIL-101"
    )
    sample_2 = st.session_state.risk_engine.analyze_email(
        "Your appointment is confirmed for next Tuesday at 2 PM. See you then!",
        analysis_id="EMAIL-102"
    )
    sample_3 = st.session_state.risk_engine.analyze_email(
        "Your account will be suspended unless you verify your details. Click here to verify: http://192.168.1.1/login",
        analysis_id="EMAIL-103"
    )

    for s in [sample_1, sample_2, sample_3]:
        node = AnalysisNode(
            analysis_id=s["analysis_id"],
            email_text=s["email_text"],
            predicted_class=s["ml_prediction"]["predicted_class"],
            ml_probability=s["ml_prediction"]["phishing_probability"],
            rule_score=s["rule_analysis"]["rule_score"],
            final_risk_score=s["final_risk_score"],
            risk_category=s["risk_category"],
            matched_indicators=s["rule_analysis"]["matched_indicators"],
            url_findings=s["rule_analysis"]["url_findings"],
            timestamp=s["timestamp"],
        )
        ll.append(node)

    st.session_state.history_list = ll

if "email_queue" not in st.session_state:
    st.session_state.email_queue = LinkedQueue()


# -------------------------------------------------------------
# HERO BANNER
# -------------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div>
        <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.15em; color: #38BDF8; font-weight: 700; margin-bottom: 4px;">
            CYBERSECURITY LAB // DATA STRUCTURES & ALGORITHMS
        </div>
        <h1 class="hero-title">PhishGuard CyberDefense</h1>
        <div class="hero-subtitle">Dual-Engine AI Classifier & Custom Foundational DSA Architecture</div>
    </div>
    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        <span class="status-pill"><span class="status-dot"></span> ML: TF-IDF + Logistic Reg</span>
        <span class="status-pill" style="border-color: #38BDF8; color: #38BDF8;"><span class="status-dot" style="background:#38BDF8; box-shadow:0 0 10px #38BDF8;"></span> DSA: 5 Active Structures</span>
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# MAIN NAVIGATION TABS
# -------------------------------------------------------------
tab_detect, tab_queue, tab_history, tab_dsa, tab_model = st.tabs([
    "AI Threat Scanner",
    "Live Queue Pipeline",
    "Audit Log & Merge Sort",
    "Interactive DSA Lab",
    "Model Intel & Audit",
])


# =============================================================
# TAB 1: AI THREAT SCANNER (EMAIL DETECTOR)
# =============================================================
with tab_detect:
    col_input, col_meta = st.columns([2.2, 1])

    with col_input:
        st.markdown('<div class="cyber-card"><div class="card-heading">Input Email Payload</div>', unsafe_allow_html=True)

        sample_emails = {
            "-- Type or paste custom email content below --": "",
            "Phishing 1: Urgent Billing Update": "Dear client, we need you to update your billing information. Click here to proceed.",
            "Phishing 2: Account Suspension & IP Link": "Your account will be suspended unless you verify your details. Click here to verify: http://192.168.1.1/login",
            "Phishing 3: Free Gift Card Prize Bait": "Congratulations! You've won a free gift card. Click here to claim it: http://free-gift-card-portal.xyz/claim",
            "Phishing 4: Nigerian Prince Wire Transfer": "Hello, I am a prince from Nigeria and I need your help to transfer $10 million. Please reply with your bank details.",
            "Phishing 5: Security Compromise Alert": "Dear user, your account has been compromised. Please reset your password using the link below: https://security-auth-check.top/reset",
            "Legitimate 1: Interview / Application": "Your recent application has been received and is under review. Thank you for applying.",
            "Legitimate 2: Shipping Notification": "Your order has been shipped and will arrive in 3-5 business days. Thank you for shopping with us.",
            "Legitimate 3: Meeting Calendar Reminder": "Your appointment is confirmed for next Tuesday at 2 PM. See you then!",
        }

        sample_choice = st.selectbox("Load Pre-Configured Threat Vector:", list(sample_emails.keys()))
        sample_text = sample_emails[sample_choice]

        user_email = st.text_area(
            "Raw Email Text:",
            value=sample_text,
            height=130,
            placeholder="Paste raw email body here to analyze headers, content, and links..."
        )

        c_act1, c_act2 = st.columns([1.5, 3])
        with c_act1:
            scan_btn = st.button("Scan Threat Vector", type="primary", use_container_width=True)
        with c_act2:
            enqueue_btn = st.button("Enqueue to Buffer", use_container_width=False)

        if enqueue_btn and user_email.strip():
            st.session_state.email_queue.enqueue(user_email.strip())
            st.toast(f"Email added to FIFO Queue. Buffer count: {st.session_state.email_queue.size}")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_meta:
        st.markdown('<div class="cyber-card"><div class="card-heading">Engine Architecture</div>', unsafe_allow_html=True)
        st.markdown("""
        - **1. Enqueue**: Added to custom `LinkedQueue`
        - **2. ML Layer**: Scikit-Learn TF-IDF vectorizer predicts posterior probability
        - **3. DSA Trie**: Scans words with boundary protection
        - **4. DSA Hash Table**: Fetches indicator weight in $O(1)$
        - **5. URL Inspector**: Heuristically checks IP hosts & deceptive domains
        - **6. DSA List**: Appends result into `SinglyLinkedList`
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # EXECUTE SCAN
    if scan_btn:
        if not user_email.strip():
            st.warning("Please provide email text to inspect.")
        else:
            with st.spinner("Analyzing email across dual ML + DSA threat vectors..."):
                engine: RiskEngine = st.session_state.risk_engine
                result = engine.analyze_email(user_email)

                # Append to persistent linked list
                node = AnalysisNode(
                    analysis_id=result["analysis_id"],
                    email_text=result["email_text"],
                    predicted_class=result["ml_prediction"]["predicted_class"],
                    ml_probability=result["ml_prediction"]["phishing_probability"],
                    rule_score=result["rule_analysis"]["rule_score"],
                    final_risk_score=result["final_risk_score"],
                    risk_category=result["risk_category"],
                    matched_indicators=result["rule_analysis"]["matched_indicators"],
                    url_findings=result["rule_analysis"]["url_findings"],
                    timestamp=result["timestamp"],
                )
                st.session_state.history_list.append(node)

                # VERDICT BANNER
                is_phish = result["ml_prediction"]["predicted_class"] == 1
                if is_phish:
                    st.markdown(f"""
                    <div class="verdict-box-phish">
                        <div class="verdict-title">[ALERT] MALICIOUS PHISHING THREAT DETECTED</div>
                        <div class="verdict-desc">
                            High confidence threat signature identified. Classification: <strong>PHISHING</strong> | 
                            Aggregated Threat Index: <strong>{result['final_risk_score'] * 100:.1f} / 100 ({result['risk_category']} Risk)</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="verdict-box-legit">
                        <div class="verdict-title">[CLEAN] VERIFIED LEGITIMATE EMAIL</div>
                        <div class="verdict-desc">
                            No malicious patterns or phishing coercion detected. Classification: <strong>LEGITIMATE</strong> | 
                            Aggregated Threat Index: <strong>{result['final_risk_score'] * 100:.1f} / 100 (Safe)</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # DUAL NEON THREAT GAUGES
                g_col1, g_col2, g_col3 = st.columns(3)

                with g_col1:
                    fig_g1 = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=result['ml_prediction']['phishing_probability'] * 100,
                        number={'suffix': "%", 'font': {'color': '#F87171' if is_phish else '#34D399', 'family': 'JetBrains Mono'}},
                        title={'text': "ML Classifier Probability", 'font': {'color': '#94A3B8', 'size': 14}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': '#475569'},
                            'bar': {'color': '#EF4444' if is_phish else '#10B981'},
                            'bgcolor': '#0F172A',
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(16, 185, 129, 0.15)'},
                                {'range': [50, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
                            ],
                        }
                    ))
                    fig_g1.update_layout(template="plotly_dark", height=200, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_g1, use_container_width=True)

                with g_col2:
                    fig_g2 = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=result['rule_analysis']['rule_score'] * 100,
                        number={'suffix': "%", 'font': {'color': '#38BDF8', 'family': 'JetBrains Mono'}},
                        title={'text': "DSA Trie Keyword Score", 'font': {'color': '#94A3B8', 'size': 14}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': '#475569'},
                            'bar': {'color': '#38BDF8'},
                            'bgcolor': '#0F172A',
                            'steps': [
                                {'range': [0, 40], 'color': 'rgba(56, 189, 248, 0.1)'},
                                {'range': [40, 100], 'color': 'rgba(56, 189, 248, 0.25)'}
                            ],
                        }
                    ))
                    fig_g2.update_layout(template="plotly_dark", height=200, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_g2, use_container_width=True)

                with g_col3:
                    final_color = "#EF4444" if result['final_risk_score'] > 0.65 else ("#F59E0B" if result['final_risk_score'] > 0.3 else "#10B981")
                    fig_g3 = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=result['final_risk_score'] * 100,
                        number={'suffix': "/100", 'font': {'color': final_color, 'family': 'JetBrains Mono'}},
                        title={'text': "Aggregated Threat Index", 'font': {'color': '#94A3B8', 'size': 14}},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': '#475569'},
                            'bar': {'color': final_color},
                            'bgcolor': '#0F172A',
                            'steps': [
                                {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.15)'},
                                {'range': [30, 65], 'color': 'rgba(245, 158, 11, 0.15)'},
                                {'range': [65, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
                            ],
                        }
                    ))
                    fig_g3.update_layout(template="plotly_dark", height=200, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_g3, use_container_width=True)

                # EVIDENCE INSPECTION
                ev_col1, ev_col2 = st.columns([1.3, 1])

                with ev_col1:
                    st.markdown('<div class="cyber-card"><div class="card-heading">DSA Trie & Hash Table Findings</div>', unsafe_allow_html=True)
                    inds = result["rule_analysis"]["matched_indicators"]
                    if inds:
                        st.markdown("**Suspicious Keywords Matched in Trie:**")
                        tags_html = "".join([f'<span class="indicator-tag">[{i["category"]}] {i["term"]} (wt: {i["weight"]})</span>' for i in inds])
                        st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)

                        st.write("")
                        # Table with explanations
                        df_ind = pd.DataFrame([{
                            "Phrase": i["term"],
                            "Category": i["category_name"],
                            "Weight": i["weight"],
                            "SOC Explanation": i["explanation"]
                        } for i in inds])
                        st.dataframe(df_ind, use_container_width=True, hide_index=True)
                    else:
                        st.info("No blacklisted keywords matched in the Trie catalog.")
                    st.markdown('</div>', unsafe_allow_html=True)

                with ev_col2:
                    st.markdown('<div class="cyber-card"><div class="card-heading">URL Threat Inspector</div>', unsafe_allow_html=True)
                    urls = result["rule_analysis"]["url_findings"]
                    if urls:
                        for u in urls:
                            st.markdown(f"**URL:** `{u['url']}` (Risk: `{u['normalized_risk_score']:.2f}`)")
                            for f in u["findings"]:
                                st.markdown(f"- **[RISK] {f['heuristic']}**: {f['detail']}")
                    else:
                        st.info("No embedded web links detected in message body.")

                    st.markdown("##### Incident Response Guidance:")
                    for rec in result["recommendations"]:
                        st.markdown(f"- {rec}")
                    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================
# TAB 2: LIVE QUEUE PIPELINE (FIFO DEMO)
# =============================================================
with tab_queue:
    st.markdown('<div class="cyber-card"><div class="card-heading">FIFO Queue Processing Conveyor</div>', unsafe_allow_html=True)
    st.write("Emails entering the gateway are buffered into a **Custom Linked Queue** with $O(1)$ Enqueue and Dequeue operations.")

    q: LinkedQueue = st.session_state.email_queue

    q_ctrl1, q_ctrl2, q_ctrl3 = st.columns([2, 1, 1])
    with q_ctrl1:
        quick_msg = st.text_input("Push Email to Buffer:", placeholder="e.g. Action required: Password expiring in 2 hours")
    with q_ctrl2:
        if st.button("Enqueue (Push to Rear)", use_container_width=True):
            if quick_msg.strip():
                q.enqueue(quick_msg.strip())
                st.success("Enqueued to rear.")
                st.rerun()
    with q_ctrl3:
        if st.button("Dequeue & Scan (Pop Front)", use_container_width=True):
            if not q.is_empty():
                popped_email = q.dequeue()
                res = st.session_state.risk_engine.analyze_email(popped_email)
                node = AnalysisNode(
                    analysis_id=res["analysis_id"],
                    email_text=res["email_text"],
                    predicted_class=res["ml_prediction"]["predicted_class"],
                    ml_probability=res["ml_prediction"]["phishing_probability"],
                    rule_score=res["rule_analysis"]["rule_score"],
                    final_risk_score=res["final_risk_score"],
                    risk_category=res["risk_category"],
                    matched_indicators=res["rule_analysis"]["matched_indicators"],
                    url_findings=res["rule_analysis"]["url_findings"],
                    timestamp=res["timestamp"],
                )
                st.session_state.history_list.append(node)
                st.toast(f"Dequeued & Analyzed: {res['ml_prediction']['predicted_label']}")
                st.rerun()
            else:
                st.warning("Buffer empty.")

    st.divider()

    # Visual Queue Ribbon
    st.markdown("#### Visual Conveyor Belt:")
    items = q.to_list()
    if items:
        ribbon_html = '<div style="display: flex; align-items: center; overflow-x: auto; padding: 12px 0;">'
        ribbon_html += '<span style="color:#34D399; font-weight:800; font-family:monospace; margin-right:8px;">[FRONT / DEQUEUE] -&gt; </span>'
        for idx, item in enumerate(items):
            role_badge = "FRONT" if idx == 0 else ("REAR" if idx == len(items) - 1 else f"#{idx+1}")
            color = "#38BDF8" if idx == 0 else "#818CF8"
            ribbon_html += f"""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1.5px solid {color}; border-radius: 10px; padding: 10px 14px; min-width: 220px; max-width: 260px; margin-right: 10px; box-shadow: 0 4px 14px rgba(0,0,0,0.4);">
                <div style="font-size: 0.75rem; color: {color}; font-weight: bold; font-family: monospace;">NODE {role_badge}</div>
                <div style="font-size: 0.85rem; color: #E2E8F0; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{html.escape(item)}</div>
            </div>
            """
            if idx < len(items) - 1:
                ribbon_html += '<span class="dsa-arrow">-&gt;</span>'
        ribbon_html += '<span style="color:#818CF8; font-weight:800; font-family:monospace; margin-left:8px;"> -&gt; [REAR / ENQUEUE]</span></div>'
        st.markdown(ribbon_html, unsafe_allow_html=True)
    else:
        st.info("The Queue is currently empty. Enqueue emails above to watch the conveyor populate.")

    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================
# TAB 3: AUDIT LOG & MERGE SORT
# =============================================================
with tab_history:
    st.markdown('<div class="cyber-card"><div class="card-heading">Singly Linked List History & Merge Sort Ranking</div>', unsafe_allow_html=True)
    history: SinglyLinkedList = st.session_state.history_list
    records = history.to_list()

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #38BDF8;">{history.size}</div>
            <div class="metric-title">Active Linked Nodes</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        head_id = history._head.analysis_id if history._head else "NULL"
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #34D399; font-size: 1.4rem;">{head_id}</div>
            <div class="metric-title">HEAD Node Pointer</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        tail_id = history._tail.analysis_id if history._tail else "NULL"
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-number" style="color: #C084FC; font-size: 1.4rem;">{tail_id}</div>
            <div class="metric-title">TAIL Node Pointer</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    sort_toggle = st.checkbox("Execute Recursive Merge Sort (Rank by Descending Threat Score)", value=False)

    if records:
        if sort_toggle:
            sorted_records, trace = merge_sort_with_trace(records, descending=True)
            active_records = sorted_records
            st.success("Sorted via custom Merge Sort. High-threat items prioritized at top.")

            # Visual Plotly Horizontal Comparison Bar
            fig_bar = px.bar(
                pd.DataFrame(sorted_records),
                x="final_risk_score",
                y="analysis_id",
                orientation="h",
                color="final_risk_score",
                color_continuous_scale="Reds",
                labels={"final_risk_score": "Risk Score", "analysis_id": "Analysis ID"},
                title="Ranked Threat Severity (Highest Risk at Top)"
            )
            fig_bar.update_layout(template="plotly_dark", height=240, margin=dict(t=35, b=20, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)

            with st.expander("View Divide & Conquer Execution Log (Recursive Splits & Merges)"):
                for step in trace[:8]:
                    st.markdown(f"- **Step {step['step']} [{step['type']}]** (Depth {step['depth']}): {step['description']}")
        else:
            active_records = records

        df_display = pd.DataFrame(active_records)[["analysis_id", "timestamp", "predicted_label", "final_risk_score", "risk_category", "email_text"]]
        st.dataframe(
            df_display,
            column_config={
                "analysis_id": "Analysis ID",
                "timestamp": "Timestamp",
                "predicted_label": "Classification",
                "final_risk_score": st.column_config.ProgressColumn("Risk Score", min_value=0.0, max_value=1.0, format="%.2f"),
                "risk_category": "Category",
                "email_text": "Email Excerpt"
            },
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.write("#### Search Audit Log by ID:")
        q_id = st.text_input("Enter Analysis ID to Search:", placeholder="e.g. EMAIL-101")
        if q_id.strip():
            found = history.search_by_id(q_id.strip())
            if found:
                st.success(f"Node Found in Linked List. ID: `{found.analysis_id}` | Class: `{found.predicted_class}` | Score: `{found.final_risk_score:.2f}`")
                st.json(found.to_dict())
            else:
                st.error("Analysis ID not found in linked list history.")

    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================
# TAB 4: INTERACTIVE DSA LAB
# =============================================================
with tab_dsa:
    st.markdown('<div class="cyber-card"><div class="card-heading">Interactive Data Structures Laboratory</div>', unsafe_allow_html=True)
    st.write("Inspect, query, and manipulate our 5 custom Data Structures in real time for project evaluations.")

    dsa_mode = st.radio(
        "Select Concept to Demonstrate:",
        [
            "1. Separate Chaining Hash Table",
            "2. Suspicious Phrase Prefix Trie",
            "3. FIFO Linked Queue",
            "4. Singly Linked List Chain",
            "5. Recursive Merge Sort Algorithm"
        ],
        horizontal=True
    )
    st.divider()

    # 1. HASH TABLE
    if "Hash Table" in dsa_mode:
        ht: SeparateChainingHashTable = st.session_state.risk_engine.hash_table
        stats = ht.get_collision_stats()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Bucket Capacity", stats["capacity"])
        c2.metric("Key Count", stats["size"])
        c3.metric("Load Factor", f"{stats['load_factor']:.2f}")
        c4.metric("Collision Chains", stats["total_collisions"])

        st.write("#### Live Bucket Inspector:")
        buckets = ht.get_buckets_view()
        non_empty = [b for b in buckets if b["chain_length"] > 0]

        # Display bucket grid
        b_cols = st.columns(4)
        for i, b in enumerate(non_empty[:12]):
            with b_cols[i % 4]:
                is_coll = b["chain_length"] > 1
                card_class = "bucket-card bucket-collision" if is_coll else "bucket-card bucket-occupied"
                badge = f"{b['chain_length']} Collisions" if is_coll else "1 Entry"
                keys_str = "<br>-&gt; ".join([f"{e['key']} (wt: {e['value']['weight']})" for e in b["entries"]])
                st.markdown(f"""
                <div class="{card_class}">
                    <div style="font-size:0.75rem; color:#38BDF8; font-weight:bold;">BUCKET #{b['bucket_index']} ({badge})</div>
                    <div style="font-size:0.8rem; margin-top:4px;">-&gt; {keys_str}</div>
                </div>
                """, unsafe_allow_html=True)

        st.write("---")
        st.write("#### Interactive Hash Code Calculator:")
        h_test = st.text_input("Enter word to hash:", value="urgent wire transfer")
        if h_test:
            calc_hash = ht._hash(h_test.lower())
            st.code(f"H('{h_test}') = sum(char[i] * 31^i) % {ht.capacity} = Bucket #{calc_hash}")

    # 2. TRIE
    elif "Trie" in dsa_mode:
        trie: SuspiciousPhraseTrie = st.session_state.risk_engine.trie
        t_stats = trie.get_structure_stats()

        st.markdown("""
        **Prefix Trie Advantage**:
        Unlike costly string substring matching, the Trie verifies single and multiword phrases in $O(L)$ time.
        Crucially, our implementation enforces **Word Boundary Protection** so `"urgent"` never triggers on `"detergent"`.
        """)

        t1, t2, t3 = st.columns(3)
        t1.metric("Registered Phrases", t_stats["stored_phrases"])
        t2.metric("Total Trie Nodes", t_stats["total_nodes"])
        t3.metric("Max Branch Depth", t_stats["max_depth"])

        st.write("#### Live Prefix Search:")
        q_prefix = st.text_input("Type prefix to traverse branches:", value="click")
        if q_prefix:
            matches = trie.get_words_with_prefix(q_prefix)
            if matches:
                st.success(f"Found {len(matches)} suspicious phrase(s) with prefix '{q_prefix}':")
                for m in matches:
                    st.markdown(f"- `{m}`")
            else:
                st.warning(f"No phrases found starting with '{q_prefix}'")

    # 3. QUEUE
    elif "Queue" in dsa_mode:
        st.write("""
        **FIFO Linked Queue**:
        Maintains an $O(1)$ front and rear pointer. Elements are enqueued at the tail and dequeued from the head.
        """)
        st.code("""
  FRONT (Head) -----------------------------------> REAR (Tail)
  [ Email #1 ] ---> [ Email #2 ] ---> [ Email #3 ] ---> NULL
   (dequeue)                                      (enqueue)
        """)

    # 4. LINKED LIST
    elif "Linked List" in dsa_mode:
        st.write("""
        **Singly Linked List Chain**:
        Every email analysis is encapsulated within an `AnalysisNode` pointing to the subsequent node.
        """)
        h_nodes = st.session_state.history_list.get_nodes_view()
        chain_html = '<div style="display:flex; align-items:center; overflow-x:auto; padding:10px 0;">'
        chain_html += '<span style="color:#34D399; font-weight:bold; font-family:monospace; margin-right:6px;">HEAD -&gt;</span>'
        for n in h_nodes:
            chain_html += f"""
            <div class="dsa-node-box">
                <div style="font-size:0.75rem; color:#38BDF8;">{n['role']}</div>
                <div>{n['analysis_id']}</div>
                <div style="font-size:0.75rem; color:#94A3B8;">Risk: {n['final_risk_score']:.2f}</div>
            </div>
            <span class="dsa-arrow">-&gt;</span>
            """
        chain_html += '<span style="color:#64748B; font-weight:bold; font-family:monospace;">NULL</span></div>'
        st.markdown(chain_html, unsafe_allow_html=True)

    # 5. MERGE SORT
    elif "Merge Sort" in dsa_mode:
        st.markdown(r"""
        **Recursive Merge Sort Architecture**:
        Guaranteed $O(n \log n)$ time complexity with stable ordering and deterministic tie-breaking.
        """)
        st.code("""
                [0.2, 0.9, 0.5, 0.8]
                       /        \\
               [0.2, 0.9]      [0.5, 0.8]      <-- Divide Phase
                /     \\         /     \\
              [0.2]  [0.9]    [0.5]  [0.8]
                \\     /         \\     /
               [0.9, 0.2]      [0.8, 0.5]      <-- Merge Phase
                       \\        /
                [0.9, 0.8, 0.5, 0.2]           <-- Final Sorted Output
        """)

    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================
# TAB 5: MODEL INTEL & AUDIT
# =============================================================
with tab_model:
    st.markdown('<div class="cyber-card"><div class="card-heading">Machine Learning Intel & Dataset Quality Audit</div>', unsafe_allow_html=True)

    m_info = json.load(open(MODEL_METRICS_PATH))
    lr_metrics = m_info["logistic_regression"]["original_test_metrics"]
    q_rep = m_info["quality_report"]

    mc1, mc2 = st.columns([1, 1.2])

    with mc1:
        st.markdown("#### Classifier Specifications:")
        st.write("- **Model Pipeline**: TF-IDF (Unigrams + Bigrams) + Logistic Regression")
        st.write(f"- **Test Accuracy**: `{lr_metrics['accuracy'] * 100:.1f}%`")
        st.write(f"- **Precision**: `{lr_metrics['precision'] * 100:.1f}%`")
        st.write(f"- **Recall**: `{lr_metrics['recall'] * 100:.1f}%`")
        st.write(f"- **F1-Score**: `{lr_metrics['f1_score'] * 100:.1f}%`")
        st.write(f"- **Validation-Tuned Decision Threshold**: `0.50`")

        # Confusion Matrix Heatmap
        cm_data = lr_metrics["confusion_matrix"]["matrix"]
        fig_cm = px.imshow(
            cm_data,
            x=["Legitimate (0)", "Phishing (1)"],
            y=["Legitimate (0)", "Phishing (1)"],
            labels=dict(x="Predicted", y="Actual", color="Count"),
            text_auto=True,
            color_continuous_scale="Teal",
            title="Confusion Matrix (Untouched Test Split)"
        )
        fig_cm.update_layout(template="plotly_dark", height=240, margin=dict(t=35, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_cm, use_container_width=True)

    with mc2:
        st.markdown("#### Critical Academic Finding — Dataset Audit:")
        st.write(f"- **Source Dataset**: `{q_rep['dataset_name']}` from Hugging Face")
        st.write("- **Split Allocation**: 600 Train / 200 Validation / 200 Test (1,000 rows total)")

        st.info(f"""
        **Examiner Viva Highlight:**  
        Automated inspection revealed the dataset contains **only 20 distinct email templates** repeated across the 1,000 records.
        Because 100% of the test split templates appear in the training split, standard test accuracy trivially reaches 100%.
        
        To prove true generalization, PhishGuard constructed a **Duplicate-Aware Partition** where templates were strictly partitioned into disjoint sets.
        """)

    st.markdown('</div>', unsafe_allow_html=True)


# Footer
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.82rem; margin-top: 30px; font-family: 'JetBrains Mono', monospace;">
    PHISHGUARD // AI PHISHING DETECTION & DSA ENGINE // ACADEMIC MINI PROJECT 2026
</div>
""", unsafe_allow_html=True)
