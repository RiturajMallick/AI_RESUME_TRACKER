
import streamlit as st
import requests
import docx2txt
import pdfplumber
from transformers import pipeline

# Load AI model for resume analysis (Using Free AI)
nlp_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")

# JSearch API Key (Make sure to replace with your actual key)
JSEARCH_API_KEY = "f677772889msh1aa0d674284462ap1cf2a7jsn2f2557275e02"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# Function to calculate ATS Score (Simulated AI)
def get_ats_score(resume_text):
    result = nlp_pipeline(resume_text[:512])  # Hugging Face model limitation
    return round(result[0]['score'] * 100, 2)  # Convert to 100 scale

# Function to suggest resume improvements
def improve_resume(resume_text):
    return (
        "🔹 Optimize keywords from the job description.\n"
        "🔹 Keep your formatting clean and ATS-friendly.\n"
        "🔹 Focus on achievements rather than just job duties."
    )

# Function to get job listings from JSearch API
def get_job_listings(query, location):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {"X-RapidAPI-Key": JSEARCH_API_KEY, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
    params = {"query": query, "location": location, "num_pages": 1}

    response = requests.get(url, headers=headers, params=params)
    jobs = response.json().get("data", [])
    return jobs

# Streamlit UI
st.title("🚀 AI Resume Tracker (With JSearch API)")
st.write("Upload your resume, get an ATS score, improvement suggestions, and find jobs!")

# File Upload
uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file:
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    else:
        resume_text = extract_text_from_docx(file_path)

    # ATS Score Calculation
    ats_score = get_ats_score(resume_text)
    st.subheader("🎯 ATS Score")
    st.write(f"Your resume ATS Score: **{ats_score}** / 100")

    # Resume Improvement Suggestions
    st.subheader("🔹 AI Improvement Suggestions")
    improvement = improve_resume(resume_text)
    st.write(improvement)

    # Job Search Section
    st.subheader("🔍 Find Jobs Based on Resume Skills")
    job_query = st.text_input("Enter Job Role", "Software Engineer")
    job_location = st.text_input("Enter Location", "Remote")

    if st.button("Find Jobs"):
        jobs = get_job_listings(job_query, job_location)
        if jobs:
            for job in jobs:
                st.write(f"**{job['job_title']}**")
                st.write(f"📍 {job['job_city']}, {job['job_country']}")
                st.write(f"🔗 [Apply Here]({job['job_apply_link']})")
                st.write("---")
        else:
            st.warning("No jobs found! Try another search.")

