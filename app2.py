import streamlit as st
import docx2txt
import fitz  # PyMuPDF for PDF processing
import requests
from bs4 import BeautifulSoup

# JobSearch API Key (Replace with your actual API key)
JSEARCH_API_KEY = "f677772889msh1aa0d674284462ap1cf2a7jsn2f2557275e02"

# Function to extract text from resume
def extract_text_from_resume(file):
    ext = file.name.split(".")[-1]
    
    if ext == "pdf":
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text

    elif ext == "docx":
        return docx2txt.process(file)
    
    else:
        return "Unsupported file type"

# Function to calculate ATS Score (Simple Analysis)
def calculate_ats_score(resume_text):
    keywords = ["Python", "Machine Learning", "Data Science", "AI", "Java", "React", "SQL"]
    score = sum(1 for word in keywords if word.lower() in resume_text.lower())
    return (score / len(keywords)) * 100  # Convert to percentage

# Function to find jobs using JobSearch API
def find_jobs(resume_text):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    query = {"query": "AI Developer", "num_pages": 1}

    response = requests.get(url, headers=headers, params=query)
    
    if response.status_code == 200:
        jobs = response.json().get("data", [])
        return jobs
    else:
        return []

# Streamlit UI
st.title("AI Resume Tracker 🚀")
st.write("Upload your resume and get ATS insights + find jobs instantly!")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    resume_text = extract_text_from_resume(uploaded_file)
    ats_score = calculate_ats_score(resume_text)
    jobs = find_jobs(resume_text)

    st.subheader("📊 ATS Score")
    st.write(f"Your ATS Score: **{ats_score:.2f}%**")

    st.subheader("📋 Resume Text Extracted")
    st.write(resume_text[:500] + "...")  # Show first 500 characters

    st.subheader("💼 Job Listings")
    if jobs:
        for job in jobs[:5]:  # Show top 5 jobs
            st.write(f"**{job['job_title']}** - {job['employer_name']}")
            st.write(f"📍 Location: {job['job_city']}, {job['job_state']}")
            st.write(f"🔗 [Apply Here]({job['job_apply_link']})")
            st.write("---")
    else:
        st.write("No jobs found for your resume keywords. Try updating your resume.")

st.write("Powered by AI & JobSearch API 🚀")






  
