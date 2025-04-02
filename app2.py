import os
import spacy
import docx2txt
import requests
import PyPDF2
import streamlit as st
import re

# Ensure spaCy model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Function to extract text from resume
def extract_text_from_resume(uploaded_file):
    if uploaded_file.name.endswith(".docx"):
        return docx2txt.process(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in pdf_reader.pages])
    else:
        return None

# Function to analyze ATS score
def analyze_ats_friendly(text):
    score = 0
    feedback = []

    sections = ["experience", "education", "skills", "certifications", "projects"]
    for section in sections:
        if re.search(section, text, re.IGNORECASE):
            score += 10
        else:
            feedback.append(f"❌ Missing section: {section.capitalize()}")

    if not re.search(r'\b\d{10}\b', text) or not re.search(r'[\w.-]+@[\w.-]+', text):
        feedback.append("❌ Missing or incorrect contact information")
    else:
        score += 10

    keywords = ["Python", "Machine Learning", "AI", "Data Science", "React", "SQL", "AWS"]
    keyword_count = sum([text.lower().count(kw.lower()) for kw in keywords])
    score += min(keyword_count * 5, 20) 
    if keyword_count == 0:
        feedback.append("❌ No relevant keywords found")

    return score, feedback

# Function to extract skills
def extract_skills(resume_text):
    doc = nlp(resume_text)
    skills = set()
    job_keywords = ["Python", "Machine Learning", "Data Science", "React", "SQL", "AWS",
                    "Java", "JavaScript", "Cloud", "Kubernetes", "TensorFlow", "AI", "NLP"]
    for token in doc:
        if token.text in job_keywords:
            skills.add(token.text)
    return list(skills)

# Function to find jobs
def find_jobs():
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query": "Software Engineer in India", "page": "1", "num_pages": "1"}
    headers = {
        "X-RapidAPI-Key": "f677772889msh1aa0d674284462ap1cf2a7jsn2f2557275e02", 
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Streamlit UI
st.title("AI Resume Analyzer & Job Finder")
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    resume_text = extract_text_from_resume(uploaded_file)
    if resume_text:
        st.subheader("Extracted Resume Text")
        st.text_area("Resume Content", resume_text, height=200)
        
        ats_score, feedback = analyze_ats_friendly(resume_text)
        st.subheader(f"ATS Score: {ats_score}/100")
        for fb in feedback:
            st.warning(fb)

        extracted_skills = extract_skills(resume_text)
        st.subheader("Extracted Skills")
        st.write(", ".join(extracted_skills))

        st.subheader("Job Recommendations")
        jobs_data = find_jobs()
        if "data" in jobs_data:
            job_listings = jobs_data["data"]
            for job in job_listings[:5]:
                st.markdown(f"**{job['job_title']}** at **{job['employer_name']}**")
                st.markdown(f"📍 {job['job_city']}, {job['job_country']}")
                st.markdown(f"[Apply Here]({job['job_apply_link']})")
                st.write("---")
        else:
            st.error("No job listings found. Try again later.")


