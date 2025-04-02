# AI Resume Tracker

![AI Resume Tracker]

## 🚀 Overview
The **AI Resume Tracker** is a powerful tool that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) and find job opportunities based on their skills. It analyzes resumes, extracts skills, provides ATS score feedback, and searches for relevant job listings.

## ✨ Features
- 📝 **Upload & Parse Resumes** (PDF & DOCX)
- ✅ **ATS Score Analysis** (Identifies missing sections & keyword optimization)
- 🏆 **Skill Extraction** (Detects relevant tech & industry skills)
- 🔍 **Job Search Integration** (Fetches job listings from JSearch API)
- 📧 **Recruiter Contact Info** (If available in job listings)

## 🛠 Installation

### **1. Clone the Repository**
```bash
  git clone https://github.com/your-username/ai-resume-tracker.git
  cd ai-resume-tracker
```

### **2. Install Dependencies**
```bash
  pip install -r requirements.txt
  python -m spacy download en_core_web_sm
```

#### **requirements.txt**
Ensure the following libraries are included in your `requirements.txt`:
```
spacy
pandas
numpy
PyPDF2
docx2txt
requests
google-colab
```

## 🚀 Usage in Google Colab

### **1. Open Google Colab**
- Go to [Google Colab](https://colab.research.google.com/)
- Upload `app.py` or copy the code into a new Colab notebook

### **2. Install Required Libraries**
Run the following in a Colab cell:
```python
!pip install -r requirements.txt
!python -m spacy download en_core_web_sm
```

### **3. Upload and Analyze Resumes**
- Run the Colab notebook
- Upload your resume (PDF/DOCX)
- The AI extracts text and analyzes your ATS score
- Get skill suggestions and improvement tips
- Find job listings matching your skills

## 🔑 API Key Configuration
Replace `YOUR_RAPIDAPI_KEY` in `app.py` with your own RapidAPI key.



## 🤝 Contributing
Contributions are welcome! Feel free to **fork**, **open an issue**, or **submit a pull request**.


---

### **🌟 Star this repo if you find it useful!** ⭐

