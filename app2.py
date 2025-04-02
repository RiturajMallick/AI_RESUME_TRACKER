import streamlit as st
import PyPDF2
import docx2txt
import spacy
import requests

# Load spaCy Model
nlp = spacy.load("en_core_web_sm")

st.title("📝 AI Resume Tracker")

# Upload Resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    def extract_text(uploaded_file):
        if uploaded_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = "".join([page.extract_text() for page in pdf_reader.pages])
            return text
        elif uploaded_file.name.endswith(".docx"):
            return docx2txt.process(uploaded_file)
        return ""

    resume_text = extract_text(uploaded_file)

    def analyze_ats_score(text):
        score = 0
        feedback = []
        sections = ["experience", "education", "skills", "certifications", "projects"]
        
        for section in sections:
            if section in text.lower():
                score += 10
            else:
                feedback.append(f"❌ Missing section: {section.capitalize()}")

        if not any(keyword in text.lower() for keyword in ["email", "@", "phone"]):
            feedback.append("❌ Missing contact details")
        else:
            score += 10

        keywords = ["Python", "Machine Learning", "AI", "Data Science"]
        keyword_count = sum([text.lower().count(kw.lower()) for kw in keywords])
        score += min(keyword_count * 5, 20)

        return score, feedback

    def extract_skills(text):
        doc = nlp(text)
        skills = set()
        job_keywords = ["Python", "Machine Learning", "Data Science", "React", "SQL", "AWS",
                        "Java", "JavaScript", "Cloud", "Kubernetes", "TensorFlow", "AI", "NLP"]

        for token in doc:
            if token.text in job_keywords:
                skills.add(token.text)

        return list(skills)

    def get_job_listings():
        url = "https://jsearch.p.rapidapi.com/search"
        headers = {
            "X-RapidAPI-Key": "f677772889msh1aa0d674284462ap1cf2a7jsn2f2557275e02",
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        querystring = {"query": "Software Engineer in India", "page": "1", "num_pages": "1"}
        response = requests.get(url, headers=headers, params=querystring)
        return response.json().get("data", [])

    # Analyze ATS Score
    ats_score, feedback = analyze_ats_score(resume_text)
    skills = extract_skills(resume_text)
    job_listings = get_job_listings()

    # Display results
    st.subheader("✅ ATS Score:")
    st.write(f"Your ATS Score: {ats_score}/100")

    st.subheader("💡 Feedback & Improvements:")
    for fb in feedback:
        st.write(fb)

    st.subheader("🔍 Extracted Skills:")
    st.write(", ".join(skills))

    st.subheader("🔎 Job Listings:")
    for job in job_listings[:5]:
        st.write(f"🔹 **{job['job_title']}**")
        st.write(f"🏢 {job['employer_name']}")
        st.write(f"📍 {job['job_city']}, {job['job_country']}")
        st.write(f"🔗 [Apply Here]({job['job_apply_link']})")
        st.write("---")

