

# Importing required libraries
import re
import spacy
import requests
import docx2txt


# Upload a resume (PDF or DOCX)
uploaded = files.upload()

# Get the uploaded file name
resume_filename = list(uploaded.keys())[0]
print(f"📂 Uploaded file: {resume_filename}")

# Function to extract text from DOCX or PDF
def extract_text(resume_filename):
    if resume_filename.endswith(".pdf"):
        import fitz  # PyMuPDF
        doc = fitz.open(resume_filename)
        text = " ".join([page.get_text() for page in doc])
    elif resume_filename.endswith(".docx"):
        text = docx2txt.process(resume_filename)
    else:
        print("❌ Unsupported file format. Please upload a PDF or DOCX file.")
        return None
    return text

# Extract text from resume
resume_text = extract_text(resume_filename)

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

# Run ATS analysis
ats_score, feedback = analyze_ats_friendly(resume_text)

# Print results
print(f"\n✅ ATS Score: {ats_score}/100")
print("\n💡 Feedback & Improvements:")
for fb in feedback:
    print(fb)

# Load spaCy English NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract skills from resume text
def extract_skills(resume_text):
    doc = nlp(resume_text)
    skills = set()  # Use a set to avoid duplicates

    # Define job-related keywords (can be expanded)
    job_keywords = ["Python", "Machine Learning", "Data Science", "React", "SQL", "AWS",
                    "Java", "JavaScript", "Cloud", "Kubernetes", "TensorFlow", "AI", "NLP","Fullstack","DevOps"]

    for token in doc:
        if token.text in job_keywords:
            skills.add(token.text)

    return list(skills)

# Get skills from resume
extracted_skills = extract_skills(resume_text)
print("\n✅ Extracted Skills:", extracted_skills)

# ---------------- JOB SEARCH USING JSEARCH API ----------------
url = "https://jsearch.p.rapidapi.com/search"

querystring = {
    "query": "Software Engineer in India",
    "page": "1",
    "num_pages": "1"
}

headers = {
    "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Replace with your actual API key
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Extract and display job details
if "data" in data:
    job_listings = data["data"]

    for job in job_listings[:5]:  # Display top 5 jobs
        print(f"\n🔹 Job Title: {job['job_title']}")
        print(f"🏢 Company: {job['employer_name']}")
        print(f"📍 Location: {job['job_city']}, {job['job_country']}")
        print(f"🔗 Apply Here: {job['job_apply_link']}")

        # Check if recruiter email exists
        recruiter_email = job.get("job_publisher_contact", "Not Available")
        print(f"📧 Recruiter Email: {recruiter_email}\n")
else:
    print("❌ No job listings found. Try a different query.")








  
