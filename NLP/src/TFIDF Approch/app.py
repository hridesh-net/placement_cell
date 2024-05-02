import os
import google.generativeai as genai
from dotenv import load_dotenv
from tqdm import tqdm
import base64
import pdf2image
import io

load_dotenv()

# Configure the Maker Suit Google API from https://makersuite.google.com/app/apikey
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, resume_pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input_text, resume_pdf_content[0], prompt])
        return response.text
    except Exception as e:
        print(e)

def resume_pdf_setup(file_path):
    try:
        with open(file_path, "rb") as file:
            images = pdf2image.convert_from_bytes(file.read())

        current_page = images[0]

        img_byte_array = io.BytesIO()
        current_page.save(img_byte_array, format='JPEG')
        img_byte_array = img_byte_array.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_array).decode()  
            }
        ]
        return pdf_parts
    except Exception as e:
        print(f"Error processing PDF file {file_path}: {e}")
        return None


def analyze_resume(resume_file, job_description, prompt):
    resume_pdf_content = resume_pdf_setup(resume_file)
    print("---------------------------======================---------------")
    print(resume_pdf_content)  # Check what is returned by resume_pdf_setup
    print("step1")
    response = get_gemini_response(prompt, resume_pdf_content, job_description)
    return response 


def main(job_description, resume_folder, prompt):
    # Load job description
    with open(job_description, 'r', encoding='utf-8') as jd_file:
        job_description_text = jd_file.read()

    # Iterate through each resume in the folder
    for filename in tqdm(os.listdir(resume_folder)):
        if filename.lower().endswith(".pdf"):
            resume_path = os.path.join(resume_folder, filename)
            response = analyze_resume(resume_path, job_description_text, prompt)
            print(f"Improvement Suggestions for Resume: {filename}")
            print(response)
            print()

if __name__ == "__main__":
    job_description_file_path = input("Enter the path to the job description text file: ")
    resume_folder_path = input("Enter the path to the folder containing resumes: ")
    prompt = input("Enter the prompt for analysis: ")

    main(job_description_file_path, resume_folder_path, prompt)
