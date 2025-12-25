# 📄 AI-Powered Resume Analyzer

An intelligent Streamlit-based application that automatically extracts structured information from resumes using Generative AI.

---

## 1. Project Title
**AI-Powered Resume Analyzer**

---

## 2. Brief One-Line Summary
A web application that uses AI to extract key candidate details from resumes (PDF/DOCX) and converts them into structured, downloadable data.

---

## 3. Overview
Recruiters and HR teams often deal with hundreds of resumes in unstructured formats such as PDFs and Word documents.  
This project leverages **Generative AI (Google Gemini)** to automatically read resumes, extract important details, and present them in a structured tabular format. The application is built using **Streamlit** for an interactive and user-friendly experience.

---

## 4. Problem Statement
Manual resume screening is:
- Time-consuming  
- Error-prone  
- Difficult to scale  

There is a need for an automated system that can efficiently parse resumes, extract relevant information, and organize it in a structured format for faster hiring decisions.

---

## 5. Dataset
- **Input Data:** Resumes uploaded by the user  
- **Supported Formats:**  
  - PDF (`.pdf`)  
  - Word Document (`.docx`)  
- **Upload Method:** ZIP file containing multiple resumes  

⚠️ No pre-collected dataset is used; resumes are processed dynamically.

---

## 6. Tools and Technologies
- **Programming Language:** Python  
- **Framework:** Streamlit  
- **AI Model:** Google Gemini (Generative AI)  
- **Libraries Used:**
  - `langchain`
  - `langchain_google_genai`
  - `pandas`
  - `PyPDF2`
  - `python-docx`
  - `dotenv`
  - `zipfile`

---

## 7. Methods
1. Upload ZIP file containing resumes  
2. Extract text from PDF/DOCX files  
3. Pass extracted text to Gemini AI using structured prompts  
4. Extract key fields such as:
   - Full Name  
   - Email  
   - Skills  
   - GitHub Links  
   - Professional Summary  
5. Store results in a Pandas DataFrame  
6. Display data and allow CSV download  

---

## 8. Key Insights
- AI can accurately extract structured information from unstructured resume text  
- Bulk resume processing significantly reduces screening time  
- Generative AI performs well even with varied resume formats  

---

## 9. Dashboard / Model / Output
- Interactive Streamlit dashboard  
- Real-time progress bar during resume processing  
- Tabular view of extracted resume details  
- Downloadable CSV file containing structured resume data  

---

## 10. Result & Conclusion
- The application successfully extracts structured resume information with high accuracy and presents it in an easy-to-use format.
- It significantly improves recruitment efficiency by automating resume screening and data extraction.

---

## 11. Future Work
- Resume ranking and scoring based on job descriptions
- Skill matching and candidate recommendation system
- Support for additional resume formats
- Resume deduplication
- Database integration for long-term storage
- Deployment on cloud platforms (AWS/GCP)

---

## 12. Author & Contact
- Author: Sahu Pavan
- Email: Sahupavan335@gmail.com
- LinkedIn: https://linkedin.com/in/sahu-pavan

