import sys
import os

# Add the parent directory (project root) to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.analysis import *
from app.rewriter import rewrite_sentences
from app.coverletter import generate_cover_letter
from app.report import generate_vagueness_report
from app.pdftools import *

from openai import OpenAI

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

resume = extract_text_from_pdf("C:/Users/lenovo/OneDrive/Desktop/Updated Resume.pdf")


job = f"""
Job Title: AI/ML Intern
Location: On-site – Lahore
Type: Internship (7:00 PM – 12:00 AM, Monday to Friday)
Duration: 3 Months

About Us:

Nexterse is a future-focused digital solutions company specializing in AI/ML development, custom software, CRM, UI/UX design, and cloud technologies. We work with global clients to build intelligent systems and data-driven applications that solve complex business problems and drive innovation.

Job Overview:

We are looking for a passionate and driven AI/ML Intern to join our team on-site. This 3-month internship is a unique opportunity to work closely with our AI experts, contribute to ongoing projects, and gain hands-on experience in real-world machine learning applications.

Key Responsibilities:

Assist in gathering, cleaning, and preparing datasets for model training.
Help develop and evaluate machine learning models using Python-based frameworks like TensorFlow, PyTorch, and Scikit-learn.
Conduct experiments and fine-tune model performance based on project requirements.
Stay updated with the latest developments in AI/ML and contribute insights to team discussions.
Document work clearly and contribute to technical reports and presentations.
Requirements:

Currently enrolled in or recently graduated from a program in Computer Science, Data Science, Artificial Intelligence, or a related field.
Solid programming skills in Python.
Understanding of basic machine learning algorithms and concepts (e.g., regression, classification, neural networks).
Familiarity with tools like NumPy, Pandas, Scikit-learn, TensorFlow, or PyTorch.
Strong analytical and problem-solving skills.
Comfortable working independently during evening hours on-site.
Nice to Have:

Experience with projects in Natural Language Processing (NLP), Computer Vision, or Recommendation Systems.
Familiarity with version control tools like Git.
Exposure to cloud platforms (AWS, GCP, Azure) or data visualization tools.
What We Offer:

A collaborative learning environment with mentorship from experienced AI engineers.
Real-world project exposure with the potential for impact.
Opportunity to transition into a full-time role based on performance.
How to Apply:
Send your resume to hr@nexterse.com with the subject line: “AI/ML Internship"

Job Type: Internship
"""

print("\n--- Resume Analysis ---")
text = analyze_resume(client, resume, job)
print(text)

parsed_resume_text =  parse_resume_analysis(text)
print(parsed_resume_text)

#generate_pdf(text, "Resume Analysis")

#
# rewritten_output = rewrite_sentences(client, resume)
#
#
# print("\n--- Vagueness Report ---")
# text = generate_vagueness_report(rewritten_output, resume)
# # #print(text)
# generate_pdf(text, "Vagueness Report")
#
# print("\n--- Cover Letter ---")
# text = generate_cover_letter(client, resume, job)
# #print(text)
# generate_pdf(text, "Cover Letter")
