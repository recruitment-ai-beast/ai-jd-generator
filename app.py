"""
AI Job Description Generator
Production-grade Streamlit application.
"""

import streamlit as st
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from utils.validators import validate_inputs, validate_api_key
from utils.jd_generator import generate_jd, generate_variations
from utils.export_utils import export_as_txt, export_as_pdf, export_as_docx

load_dotenv()
logging.basicConfig(level=logging.ERROR)

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="AI JD Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background-color: #050816;
        color: #E6F1FF;
    }

    section[data-testid="stSidebar"] {
        background-color: #0B1220;
        border-right: 1px solid #1E293B;
    }

    .main-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00D4FF, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .main-tagline {
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .card {
        background: #0B1220;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .section-label {
        color: #00D4FF;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    .metric-card {
        background: #0B1220;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00D4FF;
    }

    .metric-label {
        color: #94A3B8;
        font-size: 0.8rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #00D4FF, #3B82F6) !important;
        color: #050816 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        width: 100% !important;
        font-size: 1rem !important;
    }

    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px);
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background-color: #0B1220 !important;
        border: 1px solid #1E293B !important;
        color: #E6F1FF !important;
        border-radius: 8px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00D4FF !important;
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.1) !important;
    }

    .output-box {
        background: #0B1220;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 2rem;
        color: #E6F1FF;
        line-height: 1.8;
    }

    .success-badge {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid #22C55E;
        color: #22C55E;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .warning-badge {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid #F59E0B;
        color: #F59E0B;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }

    .history-item {
        background: #0B1220;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
    }

    .history-item:hover {
        border-color: #00D4FF;
    }

    .char-counter {
        color: #94A3B8;
        font-size: 0.75rem;
        text-align: right;
    }

    div[data-testid="stMarkdownContainer"] h2 {
        color: #00D4FF;
        border-bottom: 1px solid #1E293B;
        padding-bottom: 0.3rem;
        margin-top: 1.5rem;
    }

    div[data-testid="stMarkdownContainer"] h3 {
        color: #3B82F6;
        margin-top: 1rem;
    }

    .stProgress > div > div > div {
        background: linear-gradient(135deg, #00D4FF, #3B82F6) !important;
    }

    .stSlider > div > div > div {
        color: #00D4FF !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: #0B1220;
        color: #94A3B8;
        border-radius: 8px 8px 0 0;
    }

    .stTabs [aria-selected="true"] {
        background: #00D4FF !important;
        color: #050816 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Session State Init
# --------------------------------------------------

def init_session_state():
    defaults = {
        "generated_jd": None,
        "variations": {},
        "history": [],
        "job_title": "",
        "responsibilities": "",
        "skills": "",
        "experience_level": "Mid",
        "company_culture": "",
        "tone": "Professional",
        "word_count": 500,
        "generate_variations": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --------------------------------------------------
# API Key
# --------------------------------------------------

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
<div class="main-header">
    <div class="main-title">⚡ AI Job Description Generator</div>
    <div class="main-tagline">Generate high-converting, ATS-friendly job descriptions in seconds.</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Sidebar — Controls
# --------------------------------------------------

with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    if st.button("🔄 Reset All Settings", use_container_width=True):
        st.session_state.tone = "Professional"
        st.session_state.word_count = 500
        st.session_state.generate_variations = False
        st.rerun()

    st.markdown("---")

    tone = st.selectbox(
        "Tone",
        ["Professional", "Startup", "Casual", "Corporate"],
        index=["Professional", "Startup", "Casual", "Corporate"].index(
            st.session_state.tone
        )
    )
    st.session_state.tone = tone

    word_count = st.select_slider(
        "Target Word Count",
        options=[300, 500, 700, 1000],
        value=st.session_state.word_count
    )
    st.session_state.word_count = word_count

    generate_vars = st.toggle(
        "Generate A/B/C Variations",
        value=st.session_state.generate_variations
    )
    st.session_state.generate_variations = generate_vars

    st.markdown("---")
    st.markdown("### 📊 Session Stats")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.history)}</div>
            <div class="metric-label">Generated</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.variations)}</div>
            <div class="metric-label">Variations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="color: #94A3B8; font-size: 0.75rem; text-align: center;">
        Built by <strong style="color: #00D4FF;">BEAST</strong><br>
        Vertical AI Engineer<br>
        Recruitment Automation
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# Main Layout
# --------------------------------------------------

input_col, output_col = st.columns([1, 1.2], gap="large")

# --------------------------------------------------
# Left: Input Form
# --------------------------------------------------

with input_col:
    st.markdown('<div class="section-label">📋 Job Details</div>', unsafe_allow_html=True)

    job_title = st.text_input(
        "Job Title *",
        value=st.session_state.job_title,
        placeholder="e.g. Senior Python Engineer",
        key="job_title_input"
    )
    st.session_state.job_title = job_title

    responsibilities = st.text_area(
        "Key Responsibilities *",
        value=st.session_state.responsibilities,
        placeholder="• Build scalable REST APIs\n• Lead code reviews\n• Collaborate with product teams",
        height=140,
        key="resp_input"
    )
    st.session_state.responsibilities = responsibilities
    st.markdown(
        f'<div class="char-counter">{len(responsibilities)} chars</div>',
        unsafe_allow_html=True
    )

    skills = st.text_area(
        "Required Skills *",
        value=st.session_state.skills,
        placeholder="Python, FastAPI, LangChain, PostgreSQL, Docker",
        height=100,
        key="skills_input"
    )
    st.session_state.skills = skills
    st.markdown(
        f'<div class="char-counter">{len(skills)} chars</div>',
        unsafe_allow_html=True
    )

    experience_level = st.selectbox(
        "Experience Level *",
        ["Junior", "Mid", "Senior"],
        index=["Junior", "Mid", "Senior"].index(st.session_state.experience_level)
    )
    st.session_state.experience_level = experience_level

    company_culture = st.text_area(
        "Company Culture (optional)",
        value=st.session_state.company_culture,
        placeholder="e.g. Remote-first, fast-paced, mission-driven startup",
        height=80,
        key="culture_input"
    )
    st.session_state.company_culture = company_culture
    st.markdown(
        f'<div class="char-counter">{len(company_culture)} chars</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    generate_btn = st.button("⚡ Generate Job Description", use_container_width=True)

# --------------------------------------------------
# Generation Logic
# --------------------------------------------------

if generate_btn:
    
    st.session_state.generated_jd = None  # clear stale JD before regenerating
    # Validate API key
    key_valid, key_error = validate_api_key(GROQ_API_KEY or "")
    if not key_valid:
        st.error(key_error)
        st.stop()

    # Validate inputs
    inputs_valid, input_error = validate_inputs(
        job_title, responsibilities, skills, experience_level
    )
    if not inputs_valid:
        st.error(input_error)
        st.stop()

    # Generate
    with st.spinner("Generating your job description..."):
        jd = generate_jd(
            api_key=GROQ_API_KEY,
            job_title=job_title,
            responsibilities=responsibilities,
            skills=skills,
            experience_level=experience_level,
            company_culture=company_culture,
            tone=tone,
            word_count=word_count
        )

    if jd:
        st.session_state.generated_jd = jd

        # Add to history
        st.session_state.history.append({
            "title": job_title,
            "experience": experience_level,
            "tone": tone,
            "timestamp": datetime.now().strftime("%H:%M · %d %b"),
            "content": jd
        })

        # Generate variations if toggled
        if st.session_state.generate_variations:
            with st.spinner("Generating A/B/C variations..."):
                st.session_state.variations = generate_variations(
                    api_key=GROQ_API_KEY,
                    job_title=job_title,
                    responsibilities=responsibilities,
                    skills=skills,
                    experience_level=experience_level,
                    tone=tone
                )
    else:
        st.error(
            "We're having trouble generating your job description right now. "
            "Please try again in a few moments."
        )

# --------------------------------------------------
# Right: Output
# --------------------------------------------------

with output_col:
    if st.session_state.generated_jd:
        st.markdown('<div class="section-label">✅ Generated Job Description</div>', unsafe_allow_html=True)

        tabs = ["📄 Full JD"]
        if st.session_state.variations:
            tabs += ["🅰️ Version A", "🅱️ Version B", "🅲 Version C"]
        tabs.append("🕘 History")

        tab_objects = st.tabs(tabs)

        # --------------------------------------------------
        # Tab 1: Full JD
        # --------------------------------------------------
        with tab_objects[0]:
            jd_content = st.session_state.generated_jd

            # Word count metric
            word_c = len(jd_content.split())
            target = st.session_state.word_count
            diff = abs(word_c - target)
            status = "✅ On target" if diff < 100 else "⚠️ Off target"
            st.markdown(f"""
            <div style="display:flex; gap:1rem; margin-bottom:1rem; align-items:center;">
                <span class="success-badge">✓ Generated</span>
                <span style="color:#94A3B8; font-size:0.8rem;">~{word_c} words (target: {target}) {status}</span>
            </div>
            """, unsafe_allow_html=True)

            # ATS Score — extract from content
            ats_score = 85  # default
            for line in jd_content.split("\n"):
                if "ATS Score" in line and "/" in line:
                    try:
                        ats_score = int(line.split(":")[1].strip().split("/")[0])
                    except Exception:
                        pass

            st.markdown("**ATS Compatibility Score**")
            st.progress(ats_score / 100)
            st.markdown(
                f'<div style="color:#00D4FF; font-weight:600;">{ats_score}/100</div>',
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # Inline editable output
            edited_jd = st.text_area(
                "Edit directly below:",
                value=jd_content,
                height=500,
                key="editable_jd"
            )

            # Copy button
            if st.button("📋 Copy to Clipboard"):
                st.code(edited_jd, language="markdown")
                st.success("Content displayed above — select all and copy.")

            # Export
            st.markdown("**Export As:**")
            exp_col1, exp_col2, exp_col3 = st.columns(3)

            with exp_col1:
                txt_data = export_as_txt(edited_jd)
                st.download_button(
                    "📄 TXT",
                    data=txt_data,
                    file_name=f"{job_title.replace(' ', '_')}_JD.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with exp_col2:
                pdf_data = export_as_pdf(edited_jd, job_title)
                if pdf_data:
                    st.download_button(
                        "📕 PDF",
                        data=pdf_data,
                        file_name=f"{job_title.replace(' ', '_')}_JD.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.warning("PDF export unavailable.")

            with exp_col3:
                docx_data = export_as_docx(edited_jd, job_title)
                if docx_data:
                    st.download_button(
                        "📘 DOCX",
                        data=docx_data,
                        file_name=f"{job_title.replace(' ', '_')}_JD.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                else:
                    st.warning("DOCX export unavailable.")

        # --------------------------------------------------
        # Tabs 2-4: Variations
        # --------------------------------------------------
        if st.session_state.variations:
            for i, (label, content) in enumerate(st.session_state.variations.items()):
                with tab_objects[i + 1]:
                    st.markdown(f"**{label}**")
                    st.text_area(
                        "Edit this variation:",
                        value=content,
                        height=500,
                        key=f"var_{label}"
                    )
                    txt_var = export_as_txt(content)
                    st.download_button(
                        f"📄 Export {label}",
                        data=txt_var,
                        file_name=f"{job_title}_{label.replace(' ', '_')}.txt",
                        use_container_width=True
                    )

        # --------------------------------------------------
        # History Tab
        # --------------------------------------------------
        with tab_objects[-1]:
            if not st.session_state.history:
                st.info("No history yet. Generate your first JD above.")
            else:
                st.markdown(f"**{len(st.session_state.history)} JD(s) generated this session**")
                st.markdown("<br>", unsafe_allow_html=True)

                for i, item in enumerate(reversed(st.session_state.history)):
                    with st.expander(
                        f"📄 {item['title']} · {item['experience']} · {item['tone']} · {item['timestamp']}"
                    ):
                        st.text_area(
                            "Content:",
                            value=item["content"],
                            height=300,
                            key=f"history_{i}"
                        )
                        col_reuse, col_del = st.columns(2)

                        with col_reuse:
                            if st.button("♻️ Reuse", key=f"reuse_{i}"):
                                st.session_state.generated_jd = item["content"]
                                st.rerun()

                if st.button("🗑️ Clear History", use_container_width=True):
                    st.session_state.history = []
                    st.rerun()

    else:
        # Empty state
        st.markdown("""
        <div style="
            text-align: center;
            padding: 4rem 2rem;
            background: #0B1220;
            border: 1px dashed #1E293B;
            border-radius: 12px;
            color: #94A3B8;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #E6F1FF; margin-bottom: 0.5rem;">
                Ready to generate
            </div>
            <div style="font-size: 0.9rem;">
                Fill in the job details on the left<br>and click Generate.
            </div>
        </div>
        """, unsafe_allow_html=True)
