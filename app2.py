
import streamlit as st
import docx2txt
import fitz  # PyMuPDF
import spacy
import re
import requests

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Streamlit App UI
st.title("📄 AI Resume Tracker")
st.sidebar.header("Upload Your Resume")
uploaded_file = st.sidebar.file_uploader("Choose a resume (PDF or DOCX)", type=["pdf", "docx"])

# Function to extract text from resume
def extract_text(file):
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = " ".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)
    else:
        st.error("❌ Unsupported file format. Please upload a PDF or DOCX file.")
        return None
    return text

# Function to analyze ATS compatibility
def analyze_ats(resume_text):
    score = 0
    feedback = []
    
    # Check for key sections
    sections = ["experience", "education", "skills", "certifications", "projects"]
    for section in sections:
        if re.search(section, resume_text, re.IGNORECASE):
            score += 10
        else:
            feedback.append(f"❌ Missing: {section.capitalize()}")
    
    # Contact Info Check
    if not re.search(r'\b\d{10}\b', resume_text) or not re.search(r'[\w.-]+@[\w.-]+', resume_text):
        feedback.append("❌ Missing or incorrect contact info")
    else:
        score += 10

    # Keywords Check
    keywords = ["Python", "Machine Learning", "AI", "Data Science", "React", "SQL", "AWS", "Java"]
    keyword_count = sum([resume_text.lower().count(kw.lower()) for kw in keywords])
    score += min(keyword_count * 5, 20)
    if keyword_count == 0:
        feedback.append("❌ No relevant keywords found")

    return score, feedback

# Function to extract skills
def extract_skills(text):
    doc = nlp(text)
    skills = set()
    skill_keywords = ["Python", "Machine Learning", "Data Science", "React", "SQL", "AWS", "Java", "Cloud", "AI"]
    
    for token in doc:
        if token.text in skill_keywords:
            skills.add(token.text)
    
    return list(skills)

# Function to fetch job listings
def fetch_jobs():
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query": "Software Engineer in India", "page": "1", "num_pages": "1"}

    headers = {
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Replace with your key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    job_list = []
    if "data" in data:
        for job in data["data"][:5]:  # Get top 5 jobs
            job_list.append({
                "title": job["job_title"],
                "company": job["employer_name"],
                "location": f"{job['job_city']}, {job['job_country']}",
                "apply_link": job["job_apply_link"],
                "recruiter_email": job.get("job_publisher_contact", "Not Available")
            })
    return job_list

# Main Logic
if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    resume_text = extract_text(uploaded_file)

    if resume_text:
        st.subheader("📜 Extracted Resume Text")
        st.text_area("Resume Content", resume_text, height=200)

        # ATS Score
        ats_score, ats_feedback = analyze_ats(resume_text)
        st.subheader(f"✅ ATS Score: {ats_score}/100")
        st.write("💡 Feedback & Improvements:")
        for fb in ats_feedback:
            st.warning(fb)

        # Extracted Skills
        skills = extract_skills(resume_text)
        st.subheader("🎯 Extracted Skills")
        st.write(", ".join(skills) if skills else "No relevant skills found.")

        # Job Listings
        st.subheader("💼 Job Listings")
        jobs = fetch_jobs()
        if jobs:
            for job in jobs:
                st.markdown(f"**🔹 {job['title']}** at {job['company']}")
                st.write(f"📍 {job['location']}")
                st.write(f"🔗 [Apply Here]({job['apply_link']})")
                st.write(f"📧 Recruiter Email: {job['recruiter_email']}\n")
        else:
            st.error("❌ No job listings found.")

