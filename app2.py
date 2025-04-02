import os
import spacy
import docx2txt
import requests
import pandas as pd
import numpy as np
import re
from google.colab import files

# Ensure spaCy model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Upload a resume (PDF or DOCX)
uploaded = files.upload()
resume_filename = list(uploaded.keys())[0]

# Extract text from the uploaded file
if resume_filename.endswith(".docx"):
    resume_text = docx2txt.process(resume_filename)
elif resume_filename.endswith(".pdf"):
    import PyPDF2
    with open(resume_filename, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        resume_text = "\n".join([pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))])
else:
    print("❌ Unsupported file format. Please upload a PDF or DOCX.")
    resume_text = ""

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

    # Check for keyword optimization
    keywords = ["Python", "Machine Learning", "AI", "Data Science", "React", "SQL", "AWS"]
    keyword_count = sum([text.lower().count(kw.lower()) for kw in keywords])
    score += min(keyword_count * 5, 20)  # Max 20 points for keywords
    if keyword_count == 0:
        feedback.append("❌ No relevant keywords found")

    return score, feedback

# Run ATS analysis
ats_score, feedback = analyze_ats_friendly(resume_text)
print(f"\n✅ ATS Score: {ats_score}/100")
print("\n💡 Feedback & Improvements:")
for fb in feedback:
    print(fb)

# Function to extract skills from resume text
def extract_skills(resume_text):
    doc = nlp(resume_text)
    skills = set()  # Use a set to avoid duplicates

    # Define job-related keywords
    job_keywords = ["Python", "Machine Learning", "Data Science", "React", "SQL", "AWS",
                    "Java", "JavaScript", "Cloud", "Kubernetes", "TensorFlow", "AI", "NLP"]
    
    for token in doc:
        if token.text in job_keywords:
            skills.add(token.text)

    return list(skills)

# Get skills from the resume
extracted_skills = extract_skills(resume_text)
print("\n✅ Extracted Skills:", extracted_skills)

# Job search using RapidAPI JSearch
url = "https://jsearch.p.rapidapi.com/search"
querystring = {"query": "Software Engineer in India", "page": "1", "num_pages": "1"}

headers = {
    "X-RapidAPI-Key": "f677772889msh1aa0d674284462ap1cf2a7jsn2f2557275e02",  # Replace with your API key
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Extract and display job details
if "data" in data:
    job_listings = data["data"]
    print("\n🔥 Job Listings 🔥\n")

    for job in job_listings[:5]:  # Display top 5 jobs
        print(f"🔹 Job Title: {job['job_title']}")
        print(f"🏢 Company: {job['employer_name']}")
        print(f"📍 Location: {job['job_city']}, {job['job_country']}")
        print(f"🔗 Apply Here: {job['job_apply_link']}")

        # Check if recruiter email exists
        recruiter_email = job.get("job_publisher_contact", "Not Available")
        print(f"📧 Recruiter Email: {recruiter_email}\n")
else:
    print("❌ No job listings found. Try a different query.")




