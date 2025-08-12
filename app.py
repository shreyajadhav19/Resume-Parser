# streamlit_app.py
import streamlit as st
import fitz  # PyMuPDF
import re
import os

# ========== PDF Parsing Function ==========
def extract_info_from_pdf(pdf_file):
    text = ""
    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception:
        return {"Error": "Error reading PDF."}

    extracted_info = {
        "Name": "",
        "Email": "",
        "Phone": "",
        "Skills": []
    }

    # Extract Name (first line assumption)
    lines = text.split("\n")
    if lines:
        extracted_info["Name"] = lines[0].strip()

    # Extract Email
    email_match = re.search(r'\S+@\S+', text)
    if email_match:
        extracted_info["Email"] = email_match.group()

    # Extract Phone
    phone_match = re.search(r'(\+?\d[\d -]{8,}\d)', text)
    if phone_match:
        extracted_info["Phone"] = phone_match.group()

    # Dummy skills extraction based on keywords
    skill_keywords = ["Python", "Java", "C++", "Flask", "Django", "NLP", "SQL", "HTML", "CSS", "JavaScript"]
    found_skills = [skill for skill in skill_keywords if skill.lower() in text.lower()]
    extracted_info["Skills"] = found_skills

    return extracted_info


# ========== Streamlit UI ==========
st.set_page_config(page_title="AI Resume Parser", page_icon="📄", layout="centered")

st.title("📄 AI Resume Parser")
st.write("Upload a PDF resume to extract key details.")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting information..."):
        extracted_info = extract_info_from_pdf(uploaded_file)

    if "Error" in extracted_info:
        st.error(extracted_info["Error"])
    else:
        st.subheader("✅ Extracted Information")
        st.write(f"**Name:** {extracted_info['Name']}")
        st.write(f"**Email:** {extracted_info['Email']}")
        st.write(f"**Phone:** {extracted_info['Phone']}")
        st.write(f"**Skills:** {', '.join(extracted_info['Skills']) if extracted_info['Skills'] else 'No skills found'}")

     
