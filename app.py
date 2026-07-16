import streamlit as st
import pdfplumber
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

# 1. Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# 2. Basic NLP Skill Matcher
def extract_skills(text):
    doc = nlp(text.lower())
    # Define a default set of skills across common tech profiles (expandable)
    skills_database = {
        "python", "java", "c++", "javascript", "typescript", "html", "css", "react", 
        "node.js", "express", "sql", "postgresql", "mongodb", "aws", "docker", "kubernetes", 
        "git", "scikit-learn", "tensorflow", "pytorch", "pandas", "numpy", "tableau", 
        "powerbi", "machine learning", "deep learning", "data analysis", "nlp", "flask", "django"
    }
    
    found_skills = set()
    # Check for exact matches and common bi-grams
    for token in doc:
        if token.text in skills_database:
            found_skills.add(token.text)
            
    # Simple multi-word skill matching (like "machine learning")
    for skill in skills_database:
        if len(skill.split()) > 1 and skill in text.lower():
            found_skills.add(skill)
            
    return found_skills

# 3. Calculate ATS Score (Cosine Similarity)
def calculate_ats_score(resume_text, job_description):
    # Vectorize the documents to find overall keyword similarity
    text_list = [resume_text, job_description]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    similarity_matrix = cosine_similarity(count_matrix)
    
    # Cosine similarity score mapped to percentage
    match_percentage = round(similarity_matrix[0][1] * 100, 2)
    return match_percentage

# --- Streamlit UI ---
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")
st.subheader("Match your resume against a target job description!")

# Job Description Input
job_desc = st.text_area("🎯 Paste the Job Description here:", height=200)

# Resume File Upload
uploaded_file = st.file_uploader("📂 Upload your Resume (PDF format)", type=["pdf"])

if uploaded_file and job_desc:
    with st.spinner("Analyzing resume..."):
        # Process inputs
        resume_text = extract_text_from_pdf(uploaded_file)
        
        # Skill extraction
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_desc)
        
        # Analysis calculations
        score = calculate_ats_score(resume_text, job_desc)
        missing_skills = job_skills - resume_skills
        matching_skills = job_skills.intersection(resume_skills)
        
        # Display Results
        st.success("Analysis Complete!")
        
        # 1. ATS Score Visualization
        st.metric(label="📊 Overall ATS Match Score", value=f"{score}%")
        if score < 50:
            st.warning("⚠️ High Risk: Your resume matches less than 50% of the job description context.")
        elif score < 75:
            st.info("⚡ Moderate Match: Good progress! Adding missing keywords will push you past the threshold.")
        else:
            st.success("🎉 Excellent Match! Ready for submission.")
            
        # 2. Key Findings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Matching Skills Found")
            if matching_skills:
                for skill in matching_skills:
                    st.write(f"- `{skill.capitalize()}`")
            else:
                st.write("No matching hard skills detected.")
                
        with col2:
            st.markdown("### ❌ Missing Keywords / Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.write(f"- **{skill.capitalize()}**")
            else:
                st.write("Excellent! No major skills are missing.")

        # 3. Actionable Improvements
        st.markdown("---")
        st.markdown("### 💡 Recommended Improvements")
        
        improvements = []
        if len(resume_text.split()) < 200:
            improvements.append("Your resume seems slightly short. Consider expanding on project details and impact metrics.")
        if missing_skills:
            improvements.append(f"Incorporate the missing keywords, specifically: {', '.join([s.capitalize() for s in list(missing_skills)[:3]])}.")
        if "achieved" not in resume_text.lower() and "led" not in resume_text.lower():
            improvements.append("Add strong action verbs (e.g., *Led*, *Developed*, *Optimized*) to describe your achievements.")
            
        if improvements:
            for imp in improvements:
                st.info(imp)
        else:
            st.success("Your resume formatting and content structure look solid!")
            
else:
    st.info("💡 Please paste a job description and upload your resume PDF to begin.")