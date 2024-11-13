# import parse_resume
from src import tailor_resume
import json

def main():
    # filepath = "sample_resume.docx"
    # Parse the resume
    # parsed_data = parse_resume.parse_resume(filepath)

    # Tailor the resume
    tailored_content = tailor_resume.tailor_experience()
    print(tailored_content)

if __name__ == "__main__":
    main()
