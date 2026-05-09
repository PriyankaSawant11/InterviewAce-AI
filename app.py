"""
app.py — InterviewAce AI
Run: streamlit run app.py
"""

import streamlit as st
import json, time, os, logging
from dotenv import load_dotenv
from utils.resume_parser import extract_text_from_pdf
from nodes.collect_input import collect_input
from nodes.agent1_research import agent1_research
from nodes.agent2_coach import agent2_coach
from nodes.generate_report import generate_report

load_dotenv()

# Setup root logging so agent logs show in terminal
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

st.set_page_config(
    page_title="InterviewAce AI",  # Your unique name
    page_icon="🎯",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
    .block-container { max-width: 1100px; }
    .score-badge {
        display: inline-flex; align-items: center; gap: 8px;
        font-size: 2rem; font-weight: 800; padding: 12px 24px;
        border-radius: 12px; margin: 8px 0;
    }
    .score-high { background: linear-gradient(135deg, #d4edda, #c3e6cb); color: #155724; }
    .score-mid { background: linear-gradient(135deg, #fff3cd, #ffeaa7); color: #856404; }
    .score-low { background: linear-gradient(135deg, #f8d7da, #f5c6cb); color: #721c24; }
    .kw-match {
        display: inline-block; background: #d4edda; color: #155724;
        padding: 5px 14px; border-radius: 20px; margin: 3px; font-size: 0.85rem;
        font-weight: 600; border: 1px solid #c3e6cb;
    }
    .kw-miss {
        display: inline-block; background: #f8d7da; color: #721c24;
        padding: 5px 14px; border-radius: 20px; margin: 3px; font-size: 0.85rem;
        font-weight: 600; border: 1px solid #f5c6cb;
    }
    .info-card {
        background: #f8f9fa; border-radius: 10px; padding: 16px 20px;
        margin: 8px 0; border-left: 5px solid;
    }
    .card-blue { border-color: #4a90d9; }
    .card-purple { border-color: #7c3aed; }
    .card-green { border-color: #28a745; }
    .card-orange { border-color: #fd7e14; }
    .diff-before {
        background: #fff5f5; border-left: 4px solid #e53e3e; padding: 10px 14px;
        margin: 4px 0; border-radius: 4px; font-size: 0.88rem;
    }
    .diff-after {
        background: #f0fff4; border-left: 4px solid #38a169; padding: 10px 14px;
        margin: 4px 0; border-radius: 4px; font-size: 0.88rem;
    }
    .diff-problem { color: #e53e3e; font-size: 0.82rem; font-style: italic; margin: 2px 0 6px; }
    .priority-high { background: #dc3545; color: white; padding: 2px 10px;
                     border-radius: 10px; font-size: 0.75rem; font-weight: 700; }
    .priority-medium { background: #ffc107; color: #333; padding: 2px 10px;
                       border-radius: 10px; font-size: 0.75rem; font-weight: 700; }
    .priority-low { background: #6c757d; color: white; padding: 2px 10px;
                    border-radius: 10px; font-size: 0.75rem; font-weight: 700; }
    .q-item {
        background: #f8f9fa; padding: 10px 16px; margin: 4px 0;
        border-radius: 6px; border-left: 3px solid #4a90d9; font-size: 0.92rem;
    }
    .section-header {
        font-size: 1.3rem; font-weight: 700; margin: 24px 0 8px;
        padding-bottom: 6px; border-bottom: 2px solid #e2e8f0;
    }
    .sidebar-card {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border-radius: 12px; padding: 16px; margin: 10px 0;
        border: 1px solid #e2e8f0;
    }
    .sidebar-agent { display: flex; align-items: flex-start; gap: 10px; padding: 10px 0; }
    .sidebar-agent-icon { font-size: 1.6rem; min-width: 36px; text-align: center; }
    .sidebar-agent-text { font-size: 0.85rem; line-height: 1.4; }
    .sidebar-agent-text strong { font-size: 0.95rem; }
    .sidebar-flow {
        background: #1a1a2e; color: #e2e8f0; border-radius: 10px;
        padding: 14px; text-align: center; font-family: monospace; font-size: 0.85rem; margin: 10px 0;
    }
    .sidebar-tech { font-size: 0.75rem; color: #718096; line-height: 1.6; margin-top: 8px; }
    .loading-banner {
        background: linear-gradient(135deg, #ebf5ff, #e8f4fd);
        border: 1px solid #bee3f8; border-radius: 12px;
        padding: 20px; margin: 16px 0; text-align: center;
    }
    .loading-banner h3 { margin: 0 0 8px; color: #2b6cb0; }
    .loading-banner p { margin: 0; color: #4a5568; font-size: 0.9rem; }
    .fact-item {
        background: #f0f7ff; border-left: 4px solid #3182ce;
        padding: 10px 14px; margin: 6px 0; border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🎯 InterviewAce AI")
    st.markdown("---")
    st.markdown("""
<div class="sidebar-card">
    <div class="sidebar-agent">
        <div class="sidebar-agent-icon">🔍</div>
        <div class="sidebar-agent-text">
            <strong>Agent 1 — Researcher</strong><br>
            Searches the web using Tavily AI for company info,
            salary data, interview process, culture reviews,
            and key facts about the organization.
        </div>
    </div>
</div>
<div class="sidebar-card">
    <div class="sidebar-agent">
        <div class="sidebar-agent-icon">🎯</div>
        <div class="sidebar-agent-text">
            <strong>Agent 2 — Coach</strong><br>
            Deep-reviews your resume, generates 50 tailored
            questions, builds your prep plan, and writes
            salary negotiation scripts.
        </div>
    </div>
</div>
<div class="sidebar-flow">
    📝 Input &nbsp;→&nbsp; 🔍 Research &nbsp;→&nbsp; 🎯 Coach &nbsp;→&nbsp; 📋 Kit
</div>
<div class="sidebar-tech">
    <strong>Powered by:</strong><br>
    🧠 LangGraph — agent orchestration<br>
    🔍 Tavily — AI-powered web search<br>
    ⚡ NVIDIA NIM — Llama 3.1 70B<br>
    🚀 Groq — Llama 3.3 70B<br><br>
    <em>All free-tier APIs. No GPU needed.</em>
</div>
""", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("GenAI Lab Project — Multi-Agent Systems")

# ============================================================
# INPUTS
# ============================================================
st.markdown("# 🎯 InterviewAce AI")
st.markdown("##### *Drop your resume. Paste the JD. Get interview-ready.*")
st.divider()

c1, c2 = st.columns([1, 1], gap="large")
with c1:
    company_name = st.text_input("🏢 Company", placeholder="e.g., Google, Quantiphi, Razorpay")
    role_name = st.text_input("💼 Role", placeholder="e.g., ML Engineer, Data Scientist")
    experience_level = st.text_input("📅 Experience", placeholder="e.g., Fresher, 2 years 6 months")
with c2:
    job_description = st.text_area("📄 Job Description", placeholder="Paste the full JD...", height=195)

resume_file = st.file_uploader("📎 Resume (PDF)", type=["pdf"])
st.divider()
go = st.button("🚀 Prepare Me for the Interview", use_container_width=True, type="primary")

# ============================================================
# EXECUTION
# ============================================================
if go:
    if not company_name: st.error("Enter company name."); st.stop()
    if not role_name: st.error("Enter role."); st.stop()
    if not experience_level: st.error("Enter experience."); st.stop()
    if not job_description: st.error("Paste JD."); st.stop()
    if not resume_file: st.error("Upload resume."); st.stop()

    missing_keys = []
    if not os.getenv("NVIDIA_API_KEY"): missing_keys.append("NVIDIA_API_KEY")
    if not os.getenv("GROQ_API_KEY"): missing_keys.append("GROQ_API_KEY")
    if not os.getenv("TAVILY_API_KEY"): missing_keys.append("TAVILY_API_KEY")
    if missing_keys:
        st.error(f"Missing API keys in .env: {', '.join(missing_keys)}"); st.stop()

    resume_text = extract_text_from_pdf(resume_file.read())
    if resume_text.startswith("[ERROR]"):
        st.error(resume_text); st.stop()

    st.markdown("""
<div class="loading-banner">
    <h3>☕ Grab a coffee — this takes 3-5 minutes</h3>
    <p>Our agents are searching the web, analyzing your resume, generating 50 questions,
    and building your complete prep kit. Watch the progress below.</p>
</div>
""", unsafe_allow_html=True)

    state = {
        "company_name": company_name, "role_name": role_name,
        "job_description": job_description, "resume_text": resume_text,
        "experience_level": experience_level,
        "company_info": {}, "key_facts": [], "culture_signals": {},
        "salary_data": {}, "interview_questions": [], "jd_keywords": [],
        "red_flags": [], "competitor_companies": [], "interview_process": {},
        "company_brief": "", "resume_deep_review": {},
        "how_to_prepare": {}, "salary_strategy": "",
        "confidence_score": 0, "confidence_reasoning": "",
        "errors": [], "current_step": "starting", "final_report": "",
    }

    with st.status("🚀 Preparing your interview kit...", expanded=True) as status:
        st.write("📋 Validating inputs...")
        state.update(collect_input(state))

        if state.get("errors") and any("required" in e for e in state["errors"]):
            for e in state["errors"]: st.warning(e)
            status.update(label="❌ Validation failed", state="error"); st.stop()

        st.write("🔍 **Agent 1: Researcher** — searching with Tavily AI...")
        state.update(agent1_research(state, status_writer=st.write))

        st.write("🎯 **Agent 2: Coach** — resume review, questions, prep plan...")
        state.update(agent2_coach(state, status_writer=st.write))

        st.write("📄 Generating report...")
        state.update(generate_report(state))

        status.update(label="✅ Your prep kit is ready!", state="complete", expanded=False)

    for err in state.get("errors", []):
        st.warning(f"⚠️ {err}")

    # =========================================================
    # RENDER — ALL SECTIONS
    # =========================================================
    st.divider()

    # --- Score ---
    score = state.get("confidence_score", 0)
    cls = "score-high" if score >= 8 else ("score-mid" if score >= 5 else "score-low")
    emoji = "🟢" if score >= 8 else ("🟡" if score >= 5 else "🔴")
    st.markdown(f'<div class="score-badge {cls}">{emoji} {score}/10 Interview Ready</div>', unsafe_allow_html=True)
    reasoning = state.get("confidence_reasoning", "")
    if reasoning:
        st.markdown(f'<div class="info-card card-orange">{reasoning}</div>', unsafe_allow_html=True)
    st.divider()

    # --- Company Brief ---
    with st.expander("🏢 Company Brief & Details", expanded=True):
        brief = state.get("company_brief", "")
        if brief and brief != "Could not generate.":
            st.markdown(brief)
        else:
            st.warning("Company brief could not be generated. Check terminal logs for details.")
        ci = state.get("company_info", {})
        if ci and ci.get("what_they_do", "Unknown") != "Unknown":
            st.divider()
            a, b = st.columns(2)
            with a:
                st.markdown(f"**What they do:** {ci.get('what_they_do','N/A')}")
                st.markdown(f"**Founded:** {ci.get('founded','N/A')} · **HQ:** {ci.get('hq','N/A')}")
            with b:
                st.markdown(f"**Size:** {ci.get('size','N/A')}")
                st.markdown(f"**Business Model:** {ci.get('business_model','N/A')}")

    # --- Key Facts ---
    facts = state.get("key_facts", [])
    if facts and facts != ["No facts extracted from search results."]:
        with st.expander("💡 Key Facts & Insights"):
            for f in facts:
                st.markdown(f'<div class="fact-item">📌 {f}</div>', unsafe_allow_html=True)

    # --- Interview Process ---
    proc = state.get("interview_process", {})
    with st.expander("🔄 Interview Process & Rounds"):
        if proc.get("rounds_found"):
            a, b, c = st.columns(3)
            with a: st.metric("Rounds", proc.get("total_rounds", "?"))
            with b: st.metric("Difficulty", proc.get("overall_difficulty", "?"))
            with c: st.metric("Avg Hire Time", proc.get("avg_time_to_hire", "?"))
            st.divider()
            for rd in proc.get("rounds", []):
                if isinstance(rd, dict):
                    st.markdown(f"""<div class="info-card card-blue">
<strong>Round {rd.get('round_number','?')}: {rd.get('round_name','?')}</strong><br>
📋 Format: {rd.get('format','?')} · ⏱️ {rd.get('duration','?')}<br>
💡 <em>{rd.get('tips','')}</em></div>""", unsafe_allow_html=True)
            src = proc.get("source", "")
            if src: st.caption(f"ℹ️ Source: {src}")
        else:
            src = proc.get("source", "")
            if src:
                st.info(f"ℹ️ {src}")
            # Still show rounds if estimated
            rounds = proc.get("rounds", [])
            if rounds:
                st.markdown("**Estimated process (based on general knowledge):**")
                for rd in rounds:
                    if isinstance(rd, dict):
                        st.markdown(f"""<div class="info-card card-blue">
<strong>Round {rd.get('round_number','?')}: {rd.get('round_name','?')}</strong><br>
📋 {rd.get('format','?')} · ⏱️ {rd.get('duration','?')}<br>
💡 <em>{rd.get('tips','')}</em></div>""", unsafe_allow_html=True)

    # --- Culture ---
    culture = state.get("culture_signals", {})
    if culture and (culture.get("positives") or culture.get("negatives")):
        with st.expander("🏛️ Culture & Reviews"):
            a, b = st.columns(2)
            with a:
                st.markdown("**✅ Positives**")
                for p in culture.get("positives", []): st.markdown(f"- {p}")
            with b:
                st.markdown("**⚠️ Negatives**")
                for n in culture.get("negatives", []): st.markdown(f"- {n}")
            a2, b2 = st.columns(2)
            with a2: st.markdown(f"**Glassdoor:** {culture.get('glassdoor_score','N/A')}")
            with b2: st.markdown(f"**AmbitionBox:** {culture.get('ambitionbox_score','N/A')}")

    # --- Resume Review ---
    rev = state.get("resume_deep_review", {})
    if rev and rev.get("overall_verdict", "") != "Resume review could not be generated.":
        with st.expander("📝 Resume Review & Rewrite", expanded=True):
            verdict = rev.get("overall_verdict", "")
            if verdict:
                st.markdown(f'<div class="info-card card-orange"><strong>Overall Verdict:</strong> {verdict}</div>', unsafe_allow_html=True)
            matching = rev.get("matching_keywords", [])
            missing = rev.get("missing_keywords", [])
            if matching or missing:
                st.markdown('<div class="section-header">Keywords Analysis</div>', unsafe_allow_html=True)
                if matching:
                    st.markdown("**✅ Found in your resume:**")
                    st.markdown(" ".join([f'<span class="kw-match">{k}</span>' for k in matching]), unsafe_allow_html=True)
                if missing:
                    st.markdown("**❌ Missing — you must add these:**")
                    st.markdown(" ".join([f'<span class="kw-miss">{k}</span>' for k in missing]), unsafe_allow_html=True)
            rewrites = rev.get("bullets_to_rewrite", [])
            if rewrites:
                st.markdown('<div class="section-header">Bullets to Rewrite</div>', unsafe_allow_html=True)
                for b in rewrites:
                    if isinstance(b, dict):
                        st.markdown(f'<div class="diff-before">❌ {b.get("original","")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="diff-problem">Problem: {b.get("problem","")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="diff-after">✅ {b.get("rewritten","")}</div>', unsafe_allow_html=True)
                        kwa = b.get("keywords_added", [])
                        if kwa: st.caption(f"Keywords added: {', '.join(kwa)}")
                        st.markdown("---")
            adds = rev.get("bullets_to_add", [])
            if adds:
                st.markdown('<div class="section-header">New Bullets to Add</div>', unsafe_allow_html=True)
                for b in adds:
                    if isinstance(b, dict):
                        st.markdown(f"""<div class="info-card card-green">
<strong>➕ {b.get('suggested_bullet','')}</strong><br>
📍 Add to: {b.get('where_to_add','')}<br>
💡 {b.get('reason','')}</div>""", unsafe_allow_html=True)
            tips = rev.get("formatting_tips", [])
            if tips:
                st.markdown('<div class="section-header">Formatting Tips</div>', unsafe_allow_html=True)
                for t in tips: st.markdown(f"- {t}")

    # --- How to Prepare ---
    prep = state.get("how_to_prepare", {})
    if prep and prep.get("topics"):
        with st.expander("📚 How to Prepare"):
            summary = prep.get("summary", "")
            if summary:
                st.markdown(f'<div class="info-card card-purple">{summary}</div>', unsafe_allow_html=True)
            topics = prep.get("topics", [])
            if topics:
                st.markdown('<div class="section-header">Topics to Study</div>', unsafe_allow_html=True)
                for t in topics:
                    if isinstance(t, dict):
                        pri = t.get("priority", "MEDIUM").upper()
                        pri_cls = f"priority-{pri.lower()}" if pri in ["HIGH","MEDIUM","LOW"] else "priority-medium"
                        covers = ", ".join(t.get("what_to_cover", []))
                        resources = " · ".join(t.get("resources", []))
                        st.markdown(f"""<div class="info-card card-purple">
<strong>{t.get('topic','?')}</strong> <span class="{pri_cls}">{pri}</span> · ⏱️ {t.get('time_needed','?')}<br>
<strong>Why:</strong> {t.get('why','')}<br>
<strong>Cover:</strong> {covers}<br>
<strong>Practice:</strong> {t.get('practice','')}<br>
<strong>Resources:</strong> {resources}</div>""", unsafe_allow_html=True)
            beh = prep.get("behavioral_prep", {})
            if beh:
                st.markdown('<div class="section-header">Behavioral Prep</div>', unsafe_allow_html=True)
                st.markdown(f"**Method:** {beh.get('method','STAR')}")
                st.markdown(f"**Time:** {beh.get('time_needed','1-2 hours')}")
                for s_item in beh.get("stories_to_prepare", []): st.markdown(f"- {s_item}")
            dot = prep.get("day_of_tips", [])
            if dot:
                st.markdown('<div class="section-header">Day-of Tips</div>', unsafe_allow_html=True)
                for t in dot: st.markdown(f"- 💡 {t}")

    # --- Questions ---
    qs = state.get("interview_questions", [])
    if qs:
        with st.expander(f"🎤 Interview Questions ({len(qs)})"):
            for i, q in enumerate(qs, 1):
                st.markdown(f'<div class="q-item"><strong>{i}.</strong> {q}</div>', unsafe_allow_html=True)

    # --- Salary ---
    with st.expander("💰 Salary Strategy"):
        sd = state.get("salary_data", {})
        if sd and sd.get("verified"):
            a, b, c = st.columns(3)
            with a: st.metric("Min", sd.get("min", "N/A"))
            with b: st.metric("Average", sd.get("average", "N/A"))
            with c: st.metric("Max", sd.get("max", "N/A"))
            note = sd.get("note", "")
            if note: st.caption(f"ℹ️ {note}")
            st.divider()
        elif sd:
            st.info(f"ℹ️ {sd.get('note', 'Salary not verified.')}")
        st.markdown(state.get("salary_strategy", "N/A"))

    # --- Red Flags ---
    flags = state.get("red_flags", [])
    if flags:
        with st.expander("🚩 Red Flags"):
            for f in flags:
                st.warning(f)
    else:
        with st.expander("🚩 Red Flags"):
            st.success("✅ No red flags found in our research. This is a positive sign!")

    # --- Download ---
    st.divider()
    st.download_button("📥 Download Full Report", data=state.get("final_report", ""),
                       file_name=f"prep_{company_name.lower().replace(' ','_')}.txt",
                       mime="text/plain", use_container_width=True)