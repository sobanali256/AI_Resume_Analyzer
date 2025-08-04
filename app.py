import streamlit as st
from datetime import datetime
from app.pdftools import extract_text_from_pdf, generate_pdf_buffer
from app.analysis import analyze_resume, parse_resume_analysis
from app.coverletter import generate_cover_letter
from app.rewriter import rewrite_sentences
from app.report import generate_vagueness_report
from openai import OpenAI
# from config import OPENAI_API_KEY


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# SESSION STATE
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = {}
if 'previous_inputs' not in st.session_state:
    st.session_state.previous_inputs = {}

#  STYLING
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
hr {
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# --- PROGRESS BAR FUNCTIONS ---
def create_circular_progress(percentage, title, max_score, current_score):
    if percentage >= 80:
        color = "#10B981"
    elif percentage >= 60:
        color = "#F59E0B"
    else:
        color = "#EF4444"
    html = f"""
    <div style="text-align: center; padding: 20px;">
        <div style="position: relative; width: 120px; height: 120px; margin: 0 auto;">
            <svg width="120" height="120" style="transform: rotate(-90deg);">
                <circle cx="60" cy="60" r="50" stroke="#E5E7EB" stroke-width="8" fill="none"/>
                <circle cx="60" cy="60" r="50" stroke="{color}" stroke-width="8" fill="none"
                        stroke-dasharray="{2 * 3.14159 * 50}" 
                        stroke-dashoffset="{2 * 3.14159 * 50 * (1 - percentage / 100)}"
                        stroke-linecap="round"
                        style="transition: stroke-dashoffset 0.5s ease-in-out;"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                        font-size: 18px; font-weight: bold; color: {color};">
                {current_score}/{max_score}
            </div>
        </div>
        <div style="margin-top: 15px; font-weight: 600; color: #374151; font-size: 16px;">
            {title}
        </div>
        <div style="margin-top: 5px; font-size: 14px; color: {color}; font-weight: 500;">
            {percentage:.0f}%
        </div>
    </div>
    """
    return html


def create_overall_score_circle(score):
    percentage = score
    if percentage >= 80:
        color, grade = "#10B981", "A"
    elif percentage >= 70:
        color, grade = "#3B82F6", "B"
    elif percentage >= 60:
        color, grade = "#F59E0B", "C"
    elif percentage >= 50:
        color, grade = "#F97316", "D"
    else:
        color, grade = "#EF4444", "F"
    html = f"""
    <div style="text-align: center; padding: 30px;">
        <div style="position: relative; width: 180px; height: 180px; margin: 0 auto;">
            <svg width="180" height="180" style="transform: rotate(-90deg);">
                <circle cx="90" cy="90" r="75" stroke="#E5E7EB" stroke-width="12" fill="none"/>
                <circle cx="90" cy="90" r="75" stroke="{color}" stroke-width="12" fill="none"
                        stroke-dasharray="{2 * 3.14159 * 75}" 
                        stroke-dashoffset="{2 * 3.14159 * 75 * (1 - percentage / 100)}"
                        stroke-linecap="round"
                        style="transition: stroke-dashoffset 0.8s ease-in-out;"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                        text-align: center;">
                <div style="font-size: 36px; font-weight: bold; color: {color};">{score}</div>
                <div style="font-size: 14px; color: #6B7280; margin-top: -5px;">out of 100</div>
                <div style="font-size: 24px; font-weight: bold; color: {color}; margin-top: 5px;">Grade {grade}</div>
            </div>
        </div>
        <div style="margin-top: 15px; font-size: 18px; font-weight: 600; color: #374151;">
            Overall Resume Score
        </div>
    </div>
    """
    return html


# MAIN HEADER
st.title("AI Resume Analyzer")
st.markdown("Upload your resume and see how it stacks up for your target role.")
st.markdown("")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])


job_title = st.text_area(
    "Paste the full job title or description:",
    placeholder="Paste the complete job description here...",
    height=100
)

current_inputs = {
    'file_name': uploaded_file.name if uploaded_file else None,
    'job_title': job_title,
    'file_size': len(uploaded_file.getvalue()) if uploaded_file else None
}

if st.session_state.get('previous_inputs') != current_inputs:
    st.session_state.analysis_complete = False
    st.session_state.previous_inputs = current_inputs
    st.session_state.analysis_data = {}

if uploaded_file and job_title:
    if not st.session_state.analysis_complete:
        with st.spinner("Analyzing your resume... ⏳"):
            resume_text = extract_text_from_pdf(uploaded_file)
            raw_analysis = analyze_resume(client, resume_text, job_title)
            parsed = parse_resume_analysis(raw_analysis)
            cover_letter = generate_cover_letter(client, resume_text, job_title)
            rewritten_text = rewrite_sentences(client, resume_text)
            vagueness_output = generate_vagueness_report(rewritten_text, resume_text)

            st.session_state.analysis_data = {
                'raw_analysis': raw_analysis,
                'parsed': parsed,
                'cover_letter': cover_letter,
                'vagueness_output': vagueness_output,
                'resume_text': resume_text
            }
            st.session_state.analysis_complete = True

    if st.session_state.analysis_complete:
        data = st.session_state.analysis_data
        st.caption(f"🕒 Last analyzed: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

        # TABS
        tab1, tab2, tab3 = st.tabs(["📊 Resume Score", "✉️ Cover Letter", "📋 Vagueness Report"])

        with tab1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### 👓 Relevance Score")
                st.markdown(create_overall_score_circle(data['parsed']['total_score']), unsafe_allow_html=True)

            st.markdown("### 🔍 Detailed Breakdown")
            max_scores = {
                "Experience Match": 30,
                "Skills & Keywords": 25,
                "Achievements & Impact": 25,
                "Presentation & ATS": 20
            }
            cols = st.columns(4)
            for i, (section, score) in enumerate(data["parsed"]["breakdown"].items()):
                if score is not None:
                    max_score = max_scores[section]
                    percentage = (score / max_score) * 100
                    with cols[i]:
                        st.markdown(create_circular_progress(percentage, section, max_score, score), unsafe_allow_html=True)
                else:
                    with cols[i]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 20px;">
                            <div style="font-weight: 600; color: #6B7280;">{section}</div>
                            <div style="color: #EF4444;">No data</div>
                        </div>
                        """, unsafe_allow_html=True)

        with tab2:
            st.markdown("### 📝 Generated Cover Letter")
            st.markdown(f"""
            <div style="background-color: #F9FAFB; padding: 20px; border-radius: 10px; 
                        border: 1px solid #E5E7EB; color: #374151; font-size: 15px; line-height: 1.6;">
            {data['cover_letter'].replace('\n', '<br>')}
            </div>
            """, unsafe_allow_html=True)

        with tab3:
            st.markdown("### 🔎 Vagueness & Improvement Report")
            st.markdown(f"""
            <div style="background-color: #FFF7ED; padding: 20px; border-radius: 10px; 
                        border: 1px solid #FCD34D; color: #5B4211; font-size: 15px; line-height: 1.6;">
            {data['vagueness_output'].replace('\n', '<br>')}
            </div>
            """, unsafe_allow_html=True)

        # Downloads
        st.markdown("---")
        st.markdown("### 📥 Download Your Reports")
        col1, col2, col3 = st.columns(3)
        with col1:
            pdf1 = generate_pdf_buffer(data['raw_analysis'], f"Resume Analysis")
            st.download_button("Download Full Analysis", pdf1, file_name="resume_analysis.pdf", mime="application/pdf")
        with col2:
            pdf2 = generate_pdf_buffer(data['cover_letter'], "Cover Letter")
            st.download_button("Download Cover Letter", pdf2, file_name="cover_letter.pdf", mime="application/pdf")
        with col3:
            pdf3 = generate_pdf_buffer(data['vagueness_output'], "Vagueness Report")
            st.download_button("Download Vagueness Report", pdf3, file_name="vagueness_report.pdf", mime="application/pdf")

else:
    st.info("Please upload your resume and enter a job title to begin.")
