import streamlit as st
import docx2txt
import spacy
import subprocess
import requests
import re

# Ensure spaCy model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Function to extract text from uploaded resume
def extract_text_from_resume(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        from PyPDF2 import PdfReader
        reader = PdfReader(uploaded_file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif uploaded_file.name.endswith(".docx"):
        text = docx2txt.process(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")
    return text

# Function to analyze ATS score
def analyze_ats_friendly(text):
    score = 0
    feedback = []

    # Check for common ATS sections
    sections = ["experience", "education", "skills", "certifications", "projects"]
    for section in sections:
        if re.search(section, text, re.IGNORECASE):
            score += 10
        else:
            feedback.append(f"❌ Missing section: {section.capitalize()}")

    # Check for contact information
    if not re.search(r'\b\d{10}\b', text) or not re.search(r'[\w.-]+@[\w.-]+', text):
        feedback.append("❌ Missing or incorrect contact information")
    else:
        score += 10

    # Check for keyword optimization (example keywords)
    keywords = ["Python", "Machine Learning", "AI", "Data Science"]
    keyword_count = sum([text.lower().count(kw.lower()) for kw in keywords])
    score += min(keyword_count * 5, 20)  # Max 20 points for keywords
    if keyword_count == 0:
        feedback.append("❌ No relevant keywords found")

    return score, feedback

# Function to extract skills
def extract_skills(resume_text):
    doc = nlp(resume_text)
    skills = set()  # Use a set to avoid duplicates

    job_keywords = ["Python", "Machine Learning", "Data Science", "React", "SQL", "AWS",
                    "Java", "JavaScript", "Cloud", "Kubernetes", "TensorFlow", "AI", "NLP", "Fullstack", "DevOps"]

    for token in doc:
        if token.text in job_keywords:
            skills.add(token.text)

    return list(skills)

# Function to fetch job listings
def fetch_jobs():
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": "Software Engineer in India",
        "page": "1",
        "num_pages": "1"
    }
    headers = {
        "X-RapidAPI-Key": "f677772889msh1aa0d674284462ap1cf2a7jsn2f2557275e02",  # Replace with your API key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Streamlit UI
st.title("AI Resume Tracker & Job Finder")

uploaded_file = st.file_uploader("Upload Your Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    resume_text = extract_text_from_resume(uploaded_file)
    
    # Analyze ATS Score
    ats_score, feedback = analyze_ats_friendly(resume_text)
    extracted_skills = extract_skills(resume_text)

    st.subheader("📊 Resume Analysis")
    st.write(f"✅ **ATS Score:** {ats_score}/100")

    st.subheader("💡 Feedback & Improvements")
    for fb in feedback:
        st.write(f"- {fb}")

    st.subheader("🔍 Extracted Skills")
    st.write(", ".join(extracted_skills))

    # Fetch job listings
    st.subheader("🚀 Job Listings")
    job_data = fetch_jobs()

    if "data" in job_data:
        job_listings = job_data["data"]
        for job in job_listings[:5]:  # Show top 5 jobs
            st.write(f"🔹 **{job['job_title']}**")
            st.write(f"🏢 Company: {job['employer_name']}")
            st.write(f"📍 Location: {job['job_city']}, {job['job_country']}")
            st.write(f"🔗 [Apply Here]({job['job_apply_link']})")
            recruiter_email = job.get("job_publisher_contact", "Not Available")
            st.write(f"📧 **Recruiter Email:** {recruiter_email}")
            st.write("---")
    else:
        st.write("❌ No job listings found. Try again later.")
