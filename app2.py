import streamlit as st
import spacy
import docx2txt
import requests
import PyPDF2
import re

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Streamlit UI
st.title("📄 AI Resume Tracker")
st.write("Upload your resume and get ATS insights, job recommendations, and improvement suggestions.")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")

    # Extract text from resume
    if uploaded_file.name.endswith(".docx"):
        resume_text = docx2txt.process(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = "\n".join([pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))])
    else:
        st.error("❌ Unsupported file format. Please upload a PDF or DOCX.")

    # ATS Analysis
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

    st.subheader("✅ ATS Score")
    st.write(f"Your resume ATS score is: **{ats_score}/100**")

    st.subheader("💡 Improvements")
    for fb in feedback:
        st.write(fb)

    # Skill Extraction
    def extract_skills(resume_text):
        doc = nlp(resume_text)
        skills = set()

        job_keywords = ["Python", "Machine Learning", "Data Science", "React", "SQL", "AWS",
                        "Java", "JavaScript", "Cloud", "Kubernetes", "TensorFlow", "AI", "NLP"]

        for token in doc:
            if token.text in job_keywords:
                skills.add(token.text)

        return list(skills)

    extracted_skills = extract_skills(resume_text)
    st.subheader("🔍 Extracted Skills")
    st.write(", ".join(extracted_skills) if extracted_skills else "No skills detected.")

    # Job Search using RapidAPI
    st.subheader("🚀 Job Recommendations")

    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query": "Software Engineer in India", "page": "1", "num_pages": "1"}
    headers = {
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Replace with your API key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if "data" in data:
        job_listings = data["data"]

        for job in job_listings[:5]:  
            st.write(f"🔹 **{job['job_title']}** at **{job['employer_name']}**")
            st.write(f"📍 {job['job_city']}, {job['job_country']}")
            st.write(f"🔗 [Apply Here]({job['job_apply_link']})")
            st.write("---")
    else:
        st.write("❌ No job listings found. Try a different query.")
