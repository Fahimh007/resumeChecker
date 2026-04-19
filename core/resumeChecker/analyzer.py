import pdfplumber
from groq import Groq
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()


API_KEY = os.getenv('GROQ_API_KEY')

def analyze_resume_with_llm(resume_text:str, job_descrption:str)->dict:
    prompt = f"""
        You are an AI assistant that analyzes resumes for software engineering job applications.
        Given a resume and a job description, extract the following details:

        1. Identify all skills mentioned in the resume.
        2. Calculate the total years of experience.
           - If the resume does not mention any work experience, return the literal string
             "no experience mention" for total_experience.
        3. Categorize the projects based on the domain (e.g. AI, Web development, Cloud).
        4. Rank the resume relevance to the job description on a scale of 0 to 100.
        5. Provide a brief 2-3 sentence summary of the resume highlighting key qualifications and experience.


        Resume:
        {resume_text}

        Job Description:
        {job_descrption}

        Provide the output in valid JSON format with this structure:
        {{
            "rank" : "<percentage>",
            "skills" : ["skill", "skill2",......],
            "total_experience" : "<number of years or no experience mention>",
            "project_category" : ["category1","category2",....],
            "resume_summary" : "<2-3 sentence summary of the resume>"
        }}

        """
    #print(prompt)
    try:
        client = Groq(api_key = API_KEY)
        print(client)
        response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    response_format={"type": "json_object"},
                )
        print("#####")
        print(response)
        print("#####")
        result = response.choices[0].message.content
        return json.loads(result)

    except Exception as e:
        print(e)
        import sys, os
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def process_resume(pdf_path, job_description):
    try:
        resume_text = extract_text_from_pdf(pdf_path)
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        squared_numbers = []
        squared_numbers.extend(num ** 2 for num in numbers if num % 2 == 0)
        print(squared_numbers)

        return analyze_resume_with_llm(resume_text, job_description)
    except Exception as e:
        print(e)
        return None