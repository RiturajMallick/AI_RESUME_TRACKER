import os
import spacy
import streamlit as st
import docx2txt
import PyPDF2
import requests
import re

# Ensure spaCy model is installed
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except:
        os.system("python -m spacy download en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

st.title("📄 AI Resume Analyzer & Job Finder")
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    resume_text = ""
    
    if file_extension == "docx":
        resume_text = docx2txt.process(uploaded_file)
    elif file_extension == "pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = "\n".join([page.extract_text() for page in pdf_reader.pages])
    
    st.subheader("📌 Extracted Resume Text:")
    st.text_area("Resume Content", resume_text, height=250)
    
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
    
    ats_score, feedback = analyze_ats_friendly(resume_text)
    st.subheader("✅ ATS Score: ")
    st.write(f"**{ats_score}/100**")
    
    if feedback:
        st.subheader("💡 Feedback & Improvements:")
        for fb in feedback:
            st.write(fb)
    
    # Extract skills
    def extract_skills(text):
        doc = nlp(text)
        skills = set()
        job_keywords = ["Python", "Machine Learning", "Data Science", "React", "SQL", "AWS", "Java", "JavaScript", "Cloud", "AI"]
        for token in doc:
            if token.text in job_keywords:
                skills.add(token.text)
        return list(skills)
    
    extracted_skills = extract_skills(resume_text)
    st.subheader("✅ Extracted Skills:")
    st.write(", ".join(extracted_skills))
    
    # Job search using RapidAPI
    st.subheader("🔍 Job Listings")
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query": "Software Engineer in India", "page": "1", "num_pages": "1"}
    headers = {
        "X-RapidAPI-Key": "f677772889msh1aa0d674284462ap1cf2a7jsn2f2557275e02",  # Replace with your actual API key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    if "data" in data:
        for job in data["data"][:5]:
            st.write(f"**{job['job_title']}** at **{job['employer_name']}**")
            st.write(f"📍 {job['job_city']}, {job['job_country']}")
            st.write(f"🔗 [Apply Here]({job['job_apply_link']})")
            st.write("---")



