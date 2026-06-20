import streamlit as st
import requests

st.set_page_config(
    page_title="AI Helpdesk",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #060B18 !important;
    font-family: 'Inter', sans-serif !important;
}

header[data-testid="stHeader"], footer, #MainMenu,
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

.block-container {
    padding: 18px 32px 10px !important;
    max-width: 100% !important;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: rgba(17,24,39,0.9) !important;
    border: 1px solid rgba(75,85,99,0.4) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
}
div[data-testid="stMetricLabel"] > div {
    font-size: 0.65rem !important;
    color: #6B7280 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
div[data-testid="stMetricValue"] > div {
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #F9FAFB !important;
}

/* Inputs */
.stTextInput label, .stTextArea label {
    font-size: 0.72rem !important;
    color: #9CA3AF !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}
.stTextInput input {
    background: rgba(31,41,55,0.9) !important;
    border: 1px solid rgba(75,85,99,0.5) !important;
    border-radius: 10px !important;
    color: #F9FAFB !important;
    font-size: 0.88rem !important;
}
.stTextInput input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important;
}
.stTextArea textarea {
    background: rgba(31,41,55,0.9) !important;
    border: 1px solid rgba(75,85,99,0.5) !important;
    border-radius: 10px !important;
    color: #F9FAFB !important;
    font-size: 0.88rem !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important;
}

/* Button */
.stButton > button {
    width: 100% !important;
    height: 46px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6) !important;
    color: white !important;
    cursor: pointer !important;
    letter-spacing: 0.03em !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Success / info boxes */
.stAlert {
    border-radius: 12px !important;
    font-size: 0.82rem !important;
}

/* Divider */
hr {
    border-color: rgba(55,65,81,0.4) !important;
    margin: 8px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "submitted_email" not in st.session_state:
    st.session_state.submitted_email = ""

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-bottom:12px;">
  <h1 style="
    font-size:1.6rem; font-weight:700; margin:0; line-height:1.2;
    background:linear-gradient(90deg,#60A5FA,#A855F7);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  ">🤖 AI Helpdesk</h1>
  <p style="font-size:0.68rem; color:#4B5563; text-transform:uppercase;
     letter-spacing:0.12em; margin-top:4px;">
    Intelligent Routing &nbsp;·&nbsp; Multi-Agent AI &nbsp;·&nbsp; RAG &nbsp;·&nbsp; Groq
  </p>
</div>
""", unsafe_allow_html=True)

# ── TWO COLUMNS ───────────────────────────────────────────────────────────────
left, right = st.columns([1, 1.05], gap="large")

# ════════════════════ LEFT — FORM ═════════════════════════════════════════════
with left:
    st.markdown("""
    <div style="
      background:rgba(17,24,39,0.8);
      border:1px solid rgba(55,65,81,0.6);
      border-radius:20px; padding:20px 22px;
      backdrop-filter:blur(8px);
    ">
    <p style="font-size:0.65rem;font-weight:600;color:#6B7280;
       text-transform:uppercase;letter-spacing:0.12em;margin-bottom:10px;">
      Submit a Ticket
    </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        email = st.text_input("📧 Email Address", placeholder="john@company.com")
        feedback = st.text_area("📝 Describe your issue", height=140,
                                placeholder="e.g. VPN disconnects every few minutes…")
        submit = st.button("🚀  Submit Ticket")

    if submit:
        if not email or not feedback:
            st.warning("Please fill in both fields.")
        else:
            with st.spinner("Analyzing ticket…"):
                try:
                    response = requests.post(
                        "https://vanshhh-18-nlp-agentic.hf.space/predict",  # ✅ Fixed URL
                        json={"text": feedback, "email": email},
                        timeout=60,  # increased timeout for LLM response
                    )
                    data = response.json()
                    if "department" not in data:
                        st.error(f"Unexpected API response: {data}")
                    else:
                        st.session_state.result = data
                        st.session_state.submitted_email = email
                        st.rerun()
                except Exception as e:
                    st.error(f"Could not reach API: {e}")

    # ── feedback delivered banner (shown after submit) ────────────────────────
    if st.session_state.result:
        res_left = st.session_state.result
        st.markdown(f"""
        <div style="
          background:linear-gradient(135deg,rgba(139,92,246,.13),rgba(59,130,246,.10));
          border:1px solid rgba(139,92,246,.4);
          border-radius:14px; padding:14px 18px;
          display:flex; align-items:center; gap:14px; margin-top:10px;
        ">
          <div style="font-size:1.8rem;">📨</div>
          <div style="flex:1;">
            <div style="font-size:0.85rem;font-weight:700;color:#A855F7;margin-bottom:2px;">
              Feedback Delivered
            </div>
            <div style="font-size:0.72rem;color:#9CA3AF;">
              Your feedback has been routed to the
              <strong style="color:#E5E7EB;">{res_left.get('department', '—')}</strong>
              department &nbsp;·&nbsp; Team:
              <strong style="color:#E5E7EB;">{res_left.get('assigned_team', '—')}</strong>
            </div>
          </div>
          <div style="background:rgba(139,92,246,.2);color:#A855F7;
               font-size:0.65rem;font-weight:700;letter-spacing:0.1em;
               text-transform:uppercase;padding:4px 10px;border-radius:20px;
               white-space:nowrap;">
            ✓ Delivered
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── timeline ─────────────────────────────────────────────────────────
        steps = [
            ("✅", "Ticket received"),
            ("✅", "Department classified"),
            ("✅", "Routed to team"),
            ("✅", "RAG search completed"),
            ("✅", "AI response generated"),
            ("✅", "Confirmation email sent"),
        ]
        tl_rows = "".join(f"""
          <div style="display:flex;align-items:center;gap:10px;
               padding:5px 0;border-bottom:1px solid rgba(55,65,81,0.25);">
            <div style="width:7px;height:7px;border-radius:50%;
                 background:#10B981;box-shadow:0 0 6px #10B981;flex-shrink:0;"></div>
            <span style="font-size:0.77rem;color:#D1D5DB;font-weight:500;">{label}</span>
          </div>
        """ for _, label in steps)

        st.markdown(f"""
        <div style="
          background:rgba(17,24,39,0.7);
          border:1px solid rgba(55,65,81,0.4);
          border-radius:14px; padding:12px 16px; margin:8px 0;
        ">
          <p style="font-size:0.62rem;font-weight:600;color:#6B7280;
             text-transform:uppercase;letter-spacing:0.12em;margin-bottom:8px;">
            🔄 Timeline
          </p>
          {tl_rows}
        </div>
        """, unsafe_allow_html=True)


# ════════════════════ RIGHT — RESULTS ═════════════════════════════════════════
with right:
    res = st.session_state.result

    if res is None:
        st.markdown("""
        <div style="
          height:420px;
          background:rgba(17,24,39,0.6);
          border:1px dashed rgba(55,65,81,0.5);
          border-radius:20px;
          display:flex; flex-direction:column;
          align-items:center; justify-content:center;
          gap:10px;
        ">
          <div style="font-size:2.5rem;">🎯</div>
          <p style="font-size:0.72rem;color:#374151;
             text-transform:uppercase;letter-spacing:0.12em;">
            Results appear here
          </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── metric chips ──────────────────────────────────────────────────────
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("🏢 Department", res.get("department", "—"))
        with m2:
            st.metric("⚡ Priority", res.get("priority", "—"))
        with m3:
            st.metric("👥 Team", res.get("assigned_team", "—"))

        # ── AI response ───────────────────────────────────────────────────────
        st.markdown("""
        <p style="font-size:0.65rem;font-weight:600;color:#6B7280;
           text-transform:uppercase;letter-spacing:0.12em;margin:10px 0 4px;">
          🤖 AI Analysis
        </p>
        """, unsafe_allow_html=True)
        st.info(res.get("response", "No response available."))

        # ── confirmation banner ───────────────────────────────────────────────
        st.markdown(f"""
        <div style="
          background:linear-gradient(135deg,rgba(16,185,129,.13),rgba(59,130,246,.10));
          border:1px solid rgba(16,185,129,.4);
          border-radius:14px; padding:14px 18px;
          display:flex; align-items:center; gap:14px; margin-top:6px;
        ">
          <div style="font-size:1.8rem;">✉️</div>
          <div style="flex:1;">
            <div style="font-size:0.85rem;font-weight:700;color:#10B981;margin-bottom:2px;">
              Email Delivered
            </div>
            <div style="font-size:0.72rem;color:#9CA3AF;">
              Confirmation sent to
              <strong style="color:#E5E7EB;">{st.session_state.submitted_email}</strong>
              &nbsp;·&nbsp;
              Ticket
              <span style="background:linear-gradient(90deg,#3B82F6,#8B5CF6);
                color:white;font-size:0.65rem;font-weight:700;
                padding:2px 8px;border-radius:20px;letter-spacing:0.06em;">
                #{res.get('ticket_id', '—')}
              </span>
            </div>
          </div>
          <div style="background:rgba(16,185,129,.2);color:#10B981;
               font-size:0.65rem;font-weight:700;letter-spacing:0.1em;
               text-transform:uppercase;padding:4px 10px;border-radius:20px;
               white-space:nowrap;">
            ✓ Notified
          </div>
        </div>
        """, unsafe_allow_html=True)
