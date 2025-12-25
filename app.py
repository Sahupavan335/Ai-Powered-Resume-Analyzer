import streamlit as st
import pandas as pd
import os
import zipfile
from typing import TypedDict
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
from langchain_google_genai import ChatGoogleGenerativeAI

# ================== ENV SETUP ==================
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ================== UI STYLES ==================
st.markdown("""
<style>

/* ========== GLOBAL APP ========== */
.stApp {
    background: radial-gradient(circle at top left, #3B0F73 0%, #0B0215 35%, #000000 100%);
    color: #EDE9FE;
    font-family: 'Inter', sans-serif;
}

/* ========== SIDEBAR ========== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #120024, #050008);
    border-right: 1px solid rgba(139,92,246,0.25);
}

/* ========== HEADINGS ========== */
h1, h2, h3, h4 {
    color: #F5F3FF;
}

/* ========== TEXT ========== */
p, span, label {
    color: #C4B5FD;
}

/* ========== FILE UPLOADER ========== */
.stFileUploader {
    background: linear-gradient(180deg, rgba(30,16,60,0.8), rgba(0,0,0,0.9));
    border: 1px dashed #8B5CF6;
    border-radius: 16px;
    padding: 1.2rem;
}

/* ========== BUTTONS ========== */
.stButton > button {
    background: linear-gradient(135deg, #8B5CF6, #6366F1);
    color: #FFFFFF;
    border-radius: 999px;
    padding: 0.6rem 1.6rem;
    font-weight: 600;
    border: none;
    box-shadow: 0 0 25px rgba(139,92,246,0.6);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #A78BFA, #818CF8);
    transform: scale(1.03);
}

/* ========== DOWNLOAD BUTTON ========== */
.stDownloadButton > button {
    background: transparent;
    color: #C084FC;
    border: 1px solid #8B5CF6;
    border-radius: 999px;
}

.stDownloadButton > button:hover {
    background: #8B5CF6;
    color: #000000;
}

/* ========== DATAFRAME ========== */
[data-testid="stDataFrame"] {
    background-color: #0F0A1A;
    border-radius: 16px;
    border: 1px solid rgba(139,92,246,0.3);
}

/* ========== PROGRESS BAR ========== */
.stProgress > div > div {
    background: linear-gradient(90deg, #8B5CF6, #6366F1);
}

/* ========== INFO / SUCCESS / ERROR ========== */
.stInfo {
    background-color: rgba(30,16,60,0.6);
    border-left: 5px solid #8B5CF6;
}

.stSuccess {
    background-color: rgba(16,185,129,0.15);
    border-left: 5px solid #10B981;
}

.stError {
    background-color: rgba(239,68,68,0.15);
    border-left: 5px solid #EF4444;
}

</style>
""", unsafe_allow_html=True)


# ================== SCHEMA ==================
class Resumeschema(TypedDict):
    full_name: str
    email: str
    skills: list[str]
    github_links: str
    summary: str

# ================== TEXT EXTRACTION ==================
def extracted_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    elif file.name.endswith(".docx"):
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    return text

# ================== MAIN APP ==================
def main():

    # -------- Hero Section --------
    st.markdown(
    """
    <h1 style="
        text-align:center;
        font-size:3rem;
        font-weight:800;
        background: linear-gradient(90deg, #E9D5FF, #C084FC, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    ">
        AI-Powered Resume Analyzer
    </h1>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:#9CA3AF;'>Upload resumes • Extract insights • Download structured data</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # -------- LLM --------
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    structured_llm = llm.with_structured_output(Resumeschema)

    # -------- Upload --------
    uploader_zip = st.file_uploader(
        "Upload a ZIP file containing resumes (PDF / DOCX)",
        type=["zip"]
    )

    if uploader_zip:
        results = []

        with zipfile.ZipFile(uploader_zip, 'r') as z:
            resume_files = [f for f in z.namelist() if f.endswith(('.pdf', '.docx'))]

            if not resume_files:
                st.error("❌ No PDF or DOCX resumes found in the ZIP file.")
                return

            st.info(f"📂 Processing {len(resume_files)} resumes...")
            progress_bar = st.progress(0)

            for i, file_name in enumerate(resume_files):
                with z.open(file_name) as f:
                    raw_text = extracted_text(f)

                    response = structured_llm.invoke(
                        f"Extract key details from this resume text:\n\n{raw_text}"
                    )
                    results.append(response)

                progress_bar.progress((i + 1) / len(resume_files))

        # -------- Results --------
        if results:
            df = pd.DataFrame(results)

            st.success("✅ Resume extraction completed successfully!")
            st.dataframe(df, use_container_width=True)

            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv_data,
                file_name="resume_analysis.csv",
                mime="text/csv"
            )

# ================== RUN ==================
if __name__ == "__main__":
    main()
