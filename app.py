import streamlit as st
from prompt_grader import grade_prompt
from time import sleep

st.set_page_config(page_title="PromptGrade - Prompt Quality Evaluator", layout="centered")

st.markdown("""
    <style>
    body { background: #F7F8FB !important; }
    .stApp { font-family: 'Inter', 'Segoe UI', Arial, sans-serif; }
    .pg-headline { font-size: 2.7rem; font-weight: 900; color: #23304A; letter-spacing: 0.01em; margin-bottom: 0.15em;}
    .pg-sub { font-size: 1.17rem; color: #6D7C8B; margin-bottom: 1.7rem;}
    .stTextArea>div>textarea { border-radius: 10px !important; font-size: 1.14rem !important; background: #F1F4F9; min-height: 140px !important; font-family: 'Inter', Arial, sans-serif;}
    .stButton>button { width: 100% !important; background: linear-gradient(90deg,#4FACFE 0%,#00F2FE 100%); color: #fff !important; font-weight: 700 !important; border-radius: 10px !important; box-shadow: 0 3px 18px rgba(70, 170, 255, 0.08); transition: background 0.13s, box-shadow 0.13s;}
    .stButton>button:hover { background: linear-gradient(90deg,#00F2FE 0%,#4FACFE 100%); box-shadow: 0 6px 22px rgba(0,180,220,0.10);}
    .pg-report-zone { background: #F6FAFE; border: 2px solid #E2EEFB; border-radius: 18px; padding: 2rem 1.5rem 1.3rem 1.5rem; margin-top: 1.6rem; margin-bottom: 1.5rem; box-shadow: 0 1px 18px rgba(50, 140, 255, 0.08); animation: fadeIn .42s cubic-bezier(0.38,0.52,0.26,0.98);}
    @keyframes fadeIn { from { opacity:0; transform:translateY(24px);} to { opacity:1; transform:translateY(0);} }
    .stSpinner { color: #189AB4; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <div style="display: flex; align-items:center; gap:0.6em; margin-bottom:-1em;">
        <img src="https://cdn-icons-png.flaticon.com/512/3334/3334336.png" width="38" style="margin-right:0.22em" alt="Prompt Icon" />
        <span class="pg-headline">PromptGrade</span>
    </div>
    <div class="pg-sub">SaaS-grade evaluation for your AI prompts—clarity, structure, risk, and actionable feedback.</div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([2, 1.2])
    with col1:
        prompt = st.text_area(
            "Paste or write your prompt here:",
            height=180,
            help="A well-written prompt boosts LLM quality. Minimum 5 words for best feedback."
        )
    with col2:
        st.markdown("#### Options")
        with st.expander("Advanced", expanded=False):
            st.markdown("- **Confidential**: No prompts are saved.\n- **Scoring**: Custom NLP, readability, contradictions, clarity.")
        st.info("Rubric: Constraints, hedging/softness, contradiction risk, clarity, readability.")

    action_zone = st.empty()

    with action_zone:
        if st.button("⚡ Grade My Prompt", help="Atomic evaluation: see score and actionable feedback"):
            if not prompt.strip():
                st.error("Please enter a prompt.")
            else:
                with st.spinner("Grading in progress..."):
                    sleep(0.3)
                    result = grade_prompt(prompt)
                st.markdown(f"""
                    <div class="pg-report-zone">
                        <h3 style='margin-top:0;'>Score: <span style="font-family:monospace;font-size:1.34em;color:#2174AB;">{result['score']}/100</span> &nbsp;|&nbsp; <span style='color:#16A085'>{result['category']}</span></h3>
                        <pre style="white-space:pre-wrap;background:none;border:none;padding:0;color:#2E4157;font-size:1.09em;">
<b>Hash:</b> {result['hash']}
<b>Lines:</b> {result['lines']}
<b>Unique Tokens:</b> {result['unique_tokens']}
<b>Top Tokens:</b> {result['top_tokens']}
<b>Constraints:</b> {result['constraints']}
<b>Soft Terms (hedging):</b> {result['soft_terms']}
<b>Contradictions Detected:</b> {result['contradictions']}
<b>Sentiment/Clarity Bonus:</b> {result['sentiment_clarity']}
<b>Readability Bonus:</b> {result['readability_bonus']}
<b>Prompt Type:</b> {result['type']}
                        </pre>
                    </div>
                """, unsafe_allow_html=True)
st.caption("Built with ❤️ and atomic precision. Ultra-premium UI. Accessibility: 100% keyboard/tab navigation.")
