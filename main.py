import openai
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
overleaf_api_key = os.getenv("OVERLEAF_API_KEY")
project_id = os.getenv("OVERLEAF_PROJECT_ID")
file_path = os.getenv("OVERLEAF_FILE_PATH")

def analyze_job_description(job_description):
    """Analyze job description to extract skills and responsibilities."""
    prompt = f"Analyze the following job description and extract lists of 'skills' and 'responsibilities': {job_description}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text']

def match_resume_content(skills, experiences, job_skills, job_responsibilities):
    """Tailor resume skills and experiences to match the job description."""
    prompt = f"Match these skills {skills} and experiences {experiences} with the job skills {job_skills} and responsibilities {job_responsibilities}. Adjust wording to better fit the job description."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text']

def update_overleaf_file(latex_content):
    """Update LaTeX file on Overleaf with tailored resume content."""
    overleaf_url = f"https://api.overleaf.com/v3/projects/{project_id}/files/{file_path}"
    headers = {"Authorization": f"Bearer {overleaf_api_key}"}
    data = {"content": latex_content}
    response = requests.put(overleaf_url, headers=headers, data=data)
    return response.status_code

def compile_and_retrieve_pdf():
    """Compile the Overleaf document and get PDF download link."""
    compile_url = f"https://api.overleaf.com/v3/projects/{project_id}/compile"
    headers = {"Authorization": f"Bearer {overleaf_api_key}"}
    response = requests.post(compile_url, headers=headers)
    pdf_url = response.json().get('download_url')
    return pdf_url

def automate_resume(job_description, resume_skills, resume_experiences):
    """Main function to automate resume tailoring."""
    job_analysis = analyze_job_description(job_description)
    tailored_content = match_resume_content(resume_skills, resume_experiences, job_analysis['skills'], job_analysis['responsibilities'])
    
    latex_content = f"""
    \\section*{{Skills}}
    \\begin{{itemize}}
    {tailored_content['skills']}
    \\end{{itemize}}

    \\section*{{Experience}}
    \\begin{{itemize}}
    {tailored_content['experience']}
    \\end{{itemize}}
    """
    
    update_status = update_overleaf_file(latex_content)
    if update_status == 200:
        pdf_url = compile_and_retrieve_pdf()
        print(f"Your tailored resume is ready! Download it here: {pdf_url}")
    else:
        print("Failed to update Overleaf file.")

if __name__ == "__main__":
    job_description = "Provide job description here."
    resume_skills = "List your current skills here."
    resume_experiences = "List your current experiences here."
    
    automate_resume(job_description, resume_skills, resume_experiences)
