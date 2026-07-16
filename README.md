# 📄 AI Resume Analyzer & ATS Matcher

An interactive AI-powered web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). This tool extracts text from a PDF resume, uses Natural Language Processing (NLP) to parse technical skills, and matches them against a target job description to calculate an overall compatibility score.

🚀 **[Live App Demo Link](YOUR_STREAMLIT_APP_URL_HERE)**

---

## ✨ Features

- **PDF Text Extraction:** Seamlessly extracts structured text from multi-page PDF resumes using `pdfplumber`.
- **NLP Skill Parsing:** Analyzes both the resume and the job description using `spaCy` to extract hard and soft skills.
- **ATS Match Score:** Computes a context-aware similarity percentage utilizing Scikit-learn's Cosine Similarity algorithm.
- **Actionable Insights:** Pinpoints specific missing keywords and suggests structural improvements (e.g., action verbs, length optimization).
- **Modern UI:** Built entirely in Python with a clean, responsive `Streamlit` dashboard.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** Streamlit
- **Natural Language Processing (NLP):** spaCy (`en_core_web_sm`)
- **Text Extraction:** pdfplumber
- **Similarity Computation:** Scikit-learn (CountVectorizer & Cosine Similarity)
- **Programming Language:** Python

---

## ⚙️ How to Run Locally

Follow these steps to set up and run this application on your local machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/iifrrahakhtar/AI-Resume-Analyzer.git](https://github.com/iifrrahakhtar/AI-Resume-Analyzer.git)
cd AI-Resume-Analyzer
