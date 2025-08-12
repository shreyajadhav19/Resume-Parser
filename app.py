from flask import Flask, render_template, request
import fitz  # PyMuPDF
import os
import logging

app = Flask(__name__)

# Disable Flask and Werkzeug logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Configure uploads folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_info_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        text = "Error reading PDF."

    # Simple parsing logic (you can improve)
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
    import re
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        extracted_info = extract_info_from_pdf(filepath)

        # Pass data to result.html
        return render_template('result.html', extracted_info=extracted_info)

    return "Invalid file format. Please upload a PDF."

if __name__ == '__main__':
    import sys
    import os

    # Redirect stdout and stderr to null
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    app.run(debug=False)
