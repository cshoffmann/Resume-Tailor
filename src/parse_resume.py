from docx import Document
import fitz  # PyMuPDF
import re
import json
from dataclasses import asdict, dataclass
from typing import List
import spacy
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

@dataclass
class WorkExperience:
    title: str
    company: str
    start_date: str
    end_date: str
    responsibilities: List[str]


def parse_resume(filepath):
    """
    Parses a resume from a Word or PDF file and extracts work experience data.
    
    Parameters:
    filepath (str): The path to the resume file.
    
    Returns:
    List[WorkExperience]: A list of WorkExperience objects representing the resume's work history.
    """
    if filepath.endswith(".docx"):
        text = parse_word_resume(filepath)
    elif filepath.endswith(".pdf"):
        text = parse_pdf_resume(filepath)
    else:
        raise ValueError("Unsupported file type")

    return extract_work_experience(text)

def save_work_experience(filepath, work_experience):
    """
    Saves the work experience data to a JSON file.
    
    Parameters:
    filepath (str): The path to the output JSON file.
    work_experience (List[WorkExperience]): A list of WorkExperience objects to be saved.
    """
    data = [asdict(exp) for exp in work_experience]
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

# Parses from word docuemnts
def parse_word_resume(filepath):
    doc = Document(filepath)
    text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
    return "\n".join(text)

# Parses from pdf docuemnts
def parse_pdf_resume(filepath):
    text = ""
    with fitz.open(filepath) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            text += page.get_text("text")
    return text

def extract_work_experience(text):
    work_experience = []
    # Split by potential job experience headings
    sections = re.split(r"(?i)experience|employment|work history", text)
    if len(sections) < 2:
        return work_experience  # No experience section found
    
    experience_text = sections[1]  # Typically, the experience section is here

    # Use NLP to split by each job entry (assuming they start with titles/companies)
    doc = nlp(experience_text)
    title, company, start_date, end_date, responsibilities = "", "", "", "", []
    current_responsibilities = []

    for sent in doc.sents:
        if re.search(r"\b\d{4}\b", sent.text):  # Find sentences with dates
            if title and company:
                # Append existing job experience before starting a new one
                work_experience.append(
                    WorkExperience(title, company, start_date, end_date, current_responsibilities)
                )
                current_responsibilities = []  # Reset for the next job

            # Extract title, company, dates
            title = sent[:4].text  # Simplistic approach
            company = sent[5:10].text  # Simplistic approach
            start_date, end_date = "Start Date", "End Date"  # Adjust parsing as needed

        else:
            current_responsibilities.append(sent.text)

    # Append last job entry
    if title and company:
        work_experience.append(
            WorkExperience(title, company, start_date, end_date, current_responsibilities)
        )

    return work_experience

def get_work_experience(filepath):
    if filepath.endswith(".docx"):
        text = parse_word_resume(filepath)
    elif filepath.endswith(".pdf"):
        text = parse_pdf_resume(filepath)
    else:
        raise ValueError("Unsupported file type")

    return extract_work_experience(text)
