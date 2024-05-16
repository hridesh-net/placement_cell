from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
import base64
import pdf2image
import io

# Importing url_quote from werkzeug.utils instead of werkzeug.urls
from werkzeug.utils import url_quote

load_dotenv()
app = Flask(__name__)

# Configure the Maker Suit Google API from https://makersuite.google.com/app/apikey
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, resume_pdf_content, job_description_pdf_content, prompt):
    try:
        
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content([input_text, resume_pdf_content[0], job_description_pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return str(e)

def pdf_setup(file_path):
    try:
        with open(file_path, "rb") as file:
            images = pdf2image.convert_from_bytes(file.read())

        pdf_parts = []
        for i, image in enumerate(images):
            img_byte_array = io.BytesIO()
            image.save(img_byte_array, format='JPEG')
            img_byte_array = img_byte_array.getvalue()

            pdf_parts.append({
                "index": i,
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_array).decode()  
            })
        return pdf_parts
    except Exception as e:
        return f"Error processing PDF file {file_path}: {e}"

def analyze_resume_and_job_description(resume_content, job_description_content, job_description, prompt):
    try:
        resume_pdf_content = pdf_setup(resume_content)
        job_description_pdf_content = pdf_setup(job_description_content)

        if not resume_pdf_content or not job_description_pdf_content:
            return "Error processing resume or job description PDF."

        response = get_gemini_response(prompt, resume_pdf_content, job_description_pdf_content, prompt)
        return response 
    except Exception as e:
        return str(e)

@app.route('/analyze-resume-and-job-description', methods=['POST'])
def analyze_resume_and_job_description_api():
    if 'resume' not in request.files or 'job_description' not in request.files:
        return jsonify({'error': 'Please provide both resume and job_description files.'}), 400

    resume = request.files['resume']
    job_description = request.files['job_description']

    
    FIXED_PROMPT = "analyze me these resumes with this job descriptions and tell me hoow much percentage my resume match with job description where they lack accoding to my job description and what can i improve in my resume." 

    
    resume_content = resume.read()
    job_description_content = job_description.read()

    response = analyze_resume_and_job_description(resume_content, job_description_content, job_description.filename, FIXED_PROMPT)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
