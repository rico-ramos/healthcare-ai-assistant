from __future__ import annotations

from datetime import datetime

import streamlit as st

from healthcare_ai_assistant.config import load_settings
from healthcare_ai_assistant.runner import create_runtime

st.set_page_config(
    page_title="ClinIQ Healthcare Assistant",
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.html(
    """
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
    <style>

    /* ── Reset & Base ─────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #f0f2f7;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(14,165,233,0.08) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 110%, rgba(99,102,241,0.07) 0%, transparent 60%);
    }

    .block-container {
        padding: 1.75rem 2rem 3rem 2rem !important;
        max-width: 1340px !important;
    }

    /* ── Sidebar ──────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: #0d1117 !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.25rem 0 1.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        margin-bottom: 1.5rem;
    }

    .sidebar-logo-icon {
        width: 38px; height: 38px;
        background: linear-gradient(135deg, #0ea5e9, #6366f1);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.15rem;
        flex-shrink: 0;
    }

    .sidebar-logo-text {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 1.2rem;
        color: #f8fafc !important;
        letter-spacing: -0.02em;
    }

    .sidebar-logo-sub {
        font-size: 0.72rem;
        color: #64748b !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-weight: 500;
    }

    /* Radio pills */
    div[data-testid="stRadio"] > div {
        flex-direction: column;
        gap: 4px;
    }

    div[data-testid="stRadio"] label {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 10px !important;
        padding: 0.55rem 0.85rem !important;
        cursor: pointer;
        transition: all 0.18s;
        color: #94a3b8 !important;
        font-size: 0.875rem !important;
        font-weight: 500;
    }

    div[data-testid="stRadio"] label:hover {
        background: rgba(255,255,255,0.08) !important;
        color: #f1f5f9 !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"] {
        background: rgba(14,165,233,0.15) !important;
        border-color: rgba(14,165,233,0.4) !important;
        color: #7dd3fc !important;
    }

    /* Sidebar divider */
    hr { border-color: rgba(255,255,255,0.07) !important; }

    /* ── Hero ─────────────────────────────────────── */
    .hero {
        background: #0d1117;
        background-image:
            radial-gradient(ellipse 70% 80% at 0% 50%, rgba(14,165,233,0.18) 0%, transparent 55%),
            radial-gradient(ellipse 50% 60% at 100% 20%, rgba(99,102,241,0.15) 0%, transparent 55%);
        border-radius: 24px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .hero::before {
        content: '';
        position: absolute; inset: 0;
        background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255,255,255,0.025) 40px),
                          repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(255,255,255,0.025) 40px);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(14,165,233,0.15);
        border: 1px solid rgba(14,165,233,0.3);
        color: #38bdf8;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        padding: 0.28rem 0.75rem;
        border-radius: 999px;
        margin-bottom: 0.85rem;
    }

    .hero-badge::before { content: '●'; font-size: 0.55rem; }

    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin: 0 0 0.5rem 0;
    }

    .hero-sub {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 300;
        line-height: 1.55;
        max-width: 560px;
        margin: 0;
    }

    /* ── Metric strip ─────────────────────────────── */
    .metric-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 1.5rem;
    }

    .metric-tile {
        background: #fff;
        border: 1px solid rgba(148,163,184,0.15);
        border-radius: 18px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 12px rgba(15,23,42,0.05);
    }

    .metric-tile-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 0.35rem;
    }

    .metric-tile-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.55rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
    }

    .metric-tile-value.online { color: #059669; }

    /* ── Cards ────────────────────────────────────── */
    .card {
        background: #fff;
        border: 1px solid rgba(148,163,184,0.16);
        border-radius: 22px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(15,23,42,0.06);
        height: 100%;
    }

    .card-label {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: #0ea5e9;
        background: rgba(14,165,233,0.08);
        border: 1px solid rgba(14,165,233,0.2);
        padding: 0.22rem 0.65rem;
        border-radius: 999px;
        margin-bottom: 0.75rem;
    }

    .card-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.02em;
        margin-bottom: 1rem;
    }

    /* ── Chat Bubbles ─────────────────────────────── */
    .msg-wrap { margin-bottom: 1rem; }

    .msg-user {
        background: #f8faff;
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 18px 18px 6px 18px;
        padding: 0.9rem 1.1rem;
    }

    .msg-user-header {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #6366f1;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .msg-user-header::before { content: '👤'; font-size: 0.75rem; }

    .msg-user-body { color: #1e293b; font-size: 0.9rem; line-height: 1.55; }
    .msg-user-time { color: #94a3b8; font-size: 0.72rem; margin-top: 0.35rem; }

    .msg-ai {
        background: linear-gradient(135deg, #f0f9ff 0%, #fafffe 100%);
        border: 1px solid rgba(14,165,233,0.15);
        border-radius: 18px 18px 18px 6px;
        padding: 0.9rem 1.1rem;
        margin-top: 0.5rem;
    }

    .msg-ai-header {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #0ea5e9;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .msg-ai-header::before { content: '⚕'; font-size: 0.75rem; }

    .msg-ai-body { color: #1e293b; font-size: 0.9rem; line-height: 1.6; }

    /* ── Quick action buttons ─────────────────────── */
    .stButton button {
        border-radius: 12px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: all 0.18s !important;
    }

    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        border: none !important;
        color: #fff !important;
        box-shadow: 0 4px 14px rgba(14,165,233,0.35) !important;
        letter-spacing: 0.01em;
    }

    .stButton button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(14,165,233,0.45) !important;
        transform: translateY(-1px) !important;
    }

    .stButton button[kind="secondary"] {
        background: #f8fafc !important;
        border: 1px solid rgba(148,163,184,0.25) !important;
        color: #334155 !important;
    }

    .stButton button[kind="secondary"]:hover {
        background: #f1f5f9 !important;
        border-color: rgba(14,165,233,0.3) !important;
        color: #0ea5e9 !important;
    }

    /* ── Inputs ───────────────────────────────────── */
    .stTextArea textarea, .stSelectbox > div > div {
        border-radius: 12px !important;
        border-color: rgba(148,163,184,0.3) !important;
        background: #fafbfc !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
    }

    .stTextArea textarea:focus, .stSelectbox > div > div:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 3px rgba(14,165,233,0.1) !important;
    }

    /* ── Empty state ──────────────────────────────── */
    .empty-state {
        text-align: center;
        padding: 2.5rem 1rem;
        color: #94a3b8;
    }

    .empty-state-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        opacity: 0.5;
    }

    .empty-state-text {
        font-size: 0.9rem;
        line-height: 1.55;
    }

    /* ── Quick action chips ───────────────────────── */
    .chip-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 1.25rem;
    }

    /* ── Patient snapshot ─────────────────────────── */
    .patient-field {
        display: flex;
        align-items: baseline;
        gap: 8px;
        padding: 0.6rem 0;
        border-bottom: 1px solid rgba(148,163,184,0.12);
        font-size: 0.9rem;
    }

    .patient-field-key {
        font-weight: 600;
        color: #64748b;
        width: 90px;
        flex-shrink: 0;
        font-size: 0.8rem;
        letter-spacing: 0.02em;
    }

    .patient-field-val { color: #0f172a; }

    /* ── Status page ──────────────────────────────── */
    .status-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.75rem 1rem;
        background: #f0fdf4;
        border: 1px solid rgba(16,185,129,0.2);
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 0.9rem;
        color: #065f46;
        font-weight: 500;
    }

    .status-row::before { content: '✓'; font-weight: 700; color: #059669; }

    /* ── Scrollbar ────────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(148,163,184,0.3); border-radius: 99px; }

    /* ── Hide Streamlit chrome ────────────────────── */
    #MainMenu, footer { visibility: hidden; }

    </style>
    """
)

# ── Runtime ────────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="Initialising ClinIQ engine…")
def get_runtime():
    return create_runtime(load_settings())

for key, val in [
    ("chat_history", []),
    ("run_metrics", []),
    ("last_patient", "None"),
    ("last_action", "Ready"),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">
          <div class="sidebar-logo-icon">⚕</div>
          <div>
            <div class="sidebar-logo-text">ClinIQ</div>
            <div class="sidebar-logo-sub">AI Clinical Workspace</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    view = st.radio(
        "Navigate",
        ["Assistant", "Patient Snapshot", "System Status"],
        label_visibility="collapsed",
    )
    st.divider()
    if st.button("⟳  Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.run_metrics = []
        st.session_state.last_patient = "None"
        st.session_state.last_action = "Ready"
        st.rerun()
    st.markdown(
        """
        <div style="margin-top: auto; padding-top: 2rem;">
          <div style="font-size: 0.72rem; color: #334155; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.5rem;">Disclaimer</div>
          <div style="font-size: 0.78rem; color: #475569; line-height: 1.55;">
            For clinical staff use only. AI responses are decision-support tools — not a substitute for clinician judgment.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Hero ───────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="hero">
      <div class="hero-badge">AI-Enabled Clinical Workflow</div>
      <div class="hero-title">Modern Healthcare Assistant</div>
      <p class="hero-sub">Retrieve patient records, review medical history, book appointments, and surface evidence-based treatment guidance — all in one streamlined workspace.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Runtime init ───────────────────────────────────────────────────────────────

try:
    runtime = get_runtime()
    runtime_error = None
except Exception as exc:
    runtime = None
    runtime_error = exc

# ── Metric strip ───────────────────────────────────────────────────────────────

status_val = "Online" if runtime else "Needs setup"
status_cls = "online" if runtime else ""
patients_n = len(runtime.registry.names()) if runtime else 0
chunks_n   = runtime.stats.get("chunks", 0) if runtime else 0

st.markdown(
    f"""
    <div class="metric-strip">
      <div class="metric-tile">
        <div class="metric-tile-label">Agent Status</div>
        <div class="metric-tile-value {status_cls}">{status_val}</div>
      </div>
      <div class="metric-tile">
        <div class="metric-tile-label">Patients Loaded</div>
        <div class="metric-tile-value">{patients_n}</div>
      </div>
      <div class="metric-tile">
        <div class="metric-tile-label">Document Chunks</div>
        <div class="metric-tile-value">{chunks_n}</div>
      </div>
      <div class="metric-tile">
        <div class="metric-tile-label">Backend</div>
        <div class="metric-tile-value" style="font-size:1.1rem; padding-top:0.2rem;">LangGraph</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if runtime_error:
    st.error(f"⚠ Runtime error: {runtime_error}")
    st.info("Create a `.env` file from `.env.example`, add your `OPENAI_API_KEY`, then restart Streamlit.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# VIEW: Assistant
# ══════════════════════════════════════════════════════════════════════════════

if view == "Assistant":
    left, right = st.columns([1.7, 1], gap="medium")

    # ── Left: Chat workspace ───────────────────────────────────────────────────
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">Assistant Workspace</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Clinical Copilot</div>', unsafe_allow_html=True)

        patient_options = ["None"] + runtime.registry.names()
        prompt = st.text_area(
            "Enter request",
            placeholder="e.g. Show me the medical history for Anjali Mehra and summarize her current treatment plan.",
            height=110,
            label_visibility="collapsed",
        )
        c1, c2, c3 = st.columns([1, 1, 1.1])
        with c1:
            quick_patient = st.selectbox("Patient", patient_options, label_visibility="collapsed")
        with c2:
            quick_action = st.selectbox(
                "Action", ["Auto", "Lookup", "History", "Appointment", "Guidelines"],
                label_visibility="collapsed",
            )
        with c3:
            submit = st.button("Run Assistant →", use_container_width=True, type="primary")

        if submit and (prompt.strip() or quick_patient != "None"):
            final_prompt = prompt.strip() or f"Help with {quick_action.lower()} for {quick_patient}."
            if quick_patient != "None" and quick_patient.lower() not in final_prompt.lower():
                final_prompt += f" Patient: {quick_patient}."
            with st.spinner("ClinIQ is thinking…"):
                result = runtime.run(final_prompt)
                metrics = runtime.last_run_metrics
            st.session_state.last_patient = quick_patient if quick_patient != "None" else st.session_state.last_patient
            st.session_state.last_action = quick_action
            st.session_state.chat_history.append({
                "user": final_prompt,
                "assistant": result,
                "patient": st.session_state.last_patient,
                "timestamp": datetime.now().strftime("%I:%M %p"),
                "metrics": metrics,
            })
            st.session_state.run_metrics.append(metrics)
            st.rerun()

        st.markdown("<hr style='margin: 1rem 0; border-color: rgba(148,163,184,0.15);'>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.78rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; color:#94a3b8; margin-bottom:0.75rem;">Conversation</div>', unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown(
                """
                <div class="empty-state">
                  <div class="empty-state-icon">💬</div>
                  <div class="empty-state-text">No interactions yet.<br>Select a patient and run a request above, or use a quick action.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for item in reversed(st.session_state.chat_history):
                st.markdown(
                    f"""
                    <div class="msg-wrap">
                      <div class="msg-user">
                        <div class="msg-user-header">You</div>
                        <div class="msg-user-body">{item["user"]}</div>
                        <div class="msg-user-time">{item["timestamp"]}</div>
                      </div>
                      <div class="msg-ai">
                        <div class="msg-ai-header">ClinIQ</div>
                        <div class="msg-ai-body">{item["assistant"]}</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Right: Quick actions + notes ───────────────────────────────────────────
    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">Quick Actions</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Suggested Requests</div>', unsafe_allow_html=True)

        quick_prompts = [
            ("👤", "Look up Anjali Mehra"),
            ("📋", "Show medical history for David Thompson"),
            ("📅", "Book cardiology appointment for Ramesh Kulkarni tomorrow"),
            ("🔍", "Search treatment guidelines for upper respiratory infection"),
        ]

        for icon, qp in quick_prompts:
            if st.button(f"{icon}  {qp}", use_container_width=True):
                with st.spinner("ClinIQ is thinking…"):
                    result = runtime.run(qp)
                    metrics = runtime.last_run_metrics

                st.session_state.chat_history.append({
                    "user": qp,
                    "assistant": result,
                    "patient": st.session_state.last_patient,
                    "timestamp": datetime.now().strftime("%I:%M %p"),
                    "metrics": metrics,
                })

                st.session_state.run_metrics.append(metrics)
                st.rerun()

        st.markdown("<hr style='margin: 1rem 0; border-color: rgba(148,163,184,0.15);'>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.78rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; color:#94a3b8; margin-bottom:0.75rem;">About</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.85rem; color: #64748b; line-height: 1.65;">
              <div style="margin-bottom: 0.5rem;">⚙ <strong style="color:#334155;">LangGraph</strong> coordinates lookup, retrieval, scheduling, and synthesis tools in a unified agent loop.</div>
              <div style="margin-bottom: 0.5rem;">🔒 <strong style="color:#334155;">Staff-facing prototype.</strong> Patient data is fictional and used for demonstration only.</div>
              <div>⚕ <strong style="color:#334155;">Medical guidance</strong> is educational and does not substitute for clinician judgement.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# VIEW: Patient Snapshot
# ══════════════════════════════════════════════════════════════════════════════

elif view == "Patient Snapshot":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Patient Snapshot</div>', unsafe_allow_html=True)

    selected = st.selectbox("Select patient", runtime.registry.names())
    lookup   = runtime.registry.lookup_patient(selected)

    st.markdown(
        f'<div class="card-title" style="font-size:1.45rem; margin-bottom: 0.25rem;">{lookup.get("name", selected)}</div>',
        unsafe_allow_html=True,
    )

    fields = [
        ("Age",     lookup.get("age",     "—")),
        ("Gender",  lookup.get("gender",  "—")),
        ("Phone",   lookup.get("phone",   "—")),
        ("Address", lookup.get("address", "—")),
    ]

    for key, val in fields:
        st.markdown(
            f'<div class="patient-field"><span class="patient-field-key">{key}</span><span class="patient-field-val">{val}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; color:#94a3b8; margin-bottom:0.6rem;">Clinical Summary</div>', unsafe_allow_html=True)

    summary = lookup.get("summary", "No summary available.")
    st.markdown(
        f"""
        <div style="background: #f8faff; border: 1px solid rgba(99,102,241,0.12); border-left: 3px solid #6366f1;
                    border-radius: 12px; padding: 1rem 1.15rem; font-size: 0.9rem; color: #1e293b; line-height: 1.65;">
          {summary}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# VIEW: System Status
# ══════════════════════════════════════════════════════════════════════════════

else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">System Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Runtime Diagnostics</div>', unsafe_allow_html=True)

    docs_n = runtime.stats.get("documents", 0)

    for msg in [
        "LangGraph agent compiled successfully",
        "Patient registry loaded",
        f"{docs_n} source document(s) indexed into {chunks_n} chunk(s)",
    ]:
        st.markdown(f'<div class="status-row">{msg}</div>', unsafe_allow_html=True)

    # Runtime Metrics section starts here
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.78rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; color:#94a3b8; margin-bottom:0.6rem;">Runtime Metrics</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.run_metrics:
        st.info("No assistant runs have been measured yet.")
    else:
        latest = st.session_state.run_metrics[-1]

        avg_latency = sum(
            m["latency_seconds"] for m in st.session_state.run_metrics
        ) / len(st.session_state.run_metrics)

        total_tool_calls = sum(
            m["tool_call_count"] for m in st.session_state.run_metrics
        )

        total_tokens = sum(
            m["total_tokens"] for m in st.session_state.run_metrics
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Latest Latency", f'{latest["latency_seconds"]}s')
        c2.metric("Avg Latency", f"{avg_latency:.2f}s")
        c3.metric("Latest Tool Calls", latest["tool_call_count"])
        c4.metric("Total Tool Calls", total_tool_calls)

        st.caption(f"Total tokens this session: {total_tokens or 'N/A'}")
        st.json(latest)

    # Start command section stays below metrics
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.78rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; color:#94a3b8; margin-bottom:0.6rem;">Start command</div>',
        unsafe_allow_html=True,
    )
    st.code("streamlit run app.py", language="bash")

    st.markdown('</div>', unsafe_allow_html=True)