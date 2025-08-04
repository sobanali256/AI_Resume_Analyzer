import fitz

#Function to read form the pdf
def extract_text_from_pdf(uploaded_file):
    file_bytes = uploaded_file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    #doc = fitz.open(uploaded_file)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

#---------------------------------------

from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch

import re

def convert_markdown_to_html(text):
    # Convert **text** to <b>text</b> for bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Convert *text* to <i>text</i> for italic
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

    return text

# def generate_pdf(text, filename):
#     doc = SimpleDocTemplate(filename, pagesize=LETTER,
#                             rightMargin=72, leftMargin=72,
#                             topMargin=72, bottomMargin=72)
#
#     text = convert_markdown_to_html(text)
#     styles = getSampleStyleSheet()
#
#     # Create a custom justified paragraph style
#     justified_style = ParagraphStyle(
#         name='Justified',
#         parent=styles['Normal'],
#         fontName='Times-Roman',
#         fontSize=11,
#         leading=14,
#         alignment=TA_JUSTIFY,
#     )
#
#     heading_style = ParagraphStyle(
#         name='Heading',
#         parent=styles['Heading2'],
#         fontName='Times-Bold',
#         fontSize=14,
#         leading=16,
#         alignment=TA_LEFT,
#         spaceBefore=12,
#         spaceAfter=6,
#     )
#
#     story = []
#
#     # Split into paragraphs
#     for para in text.strip().split('\n'):
#         if para.strip():
#             story.append(Paragraph(para.strip(), justified_style))
#             story.append(Spacer(1, 12))  # 12 points = approx one line
#
#     doc.build(story)
#     print(f"✅ PDF saved as: {filename}")
#-----------------------------------------------------------------
import io

def generate_pdf_buffer(text, title="Document"):

    # Create a BytesIO buffer
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    text = convert_markdown_to_html(text)
    styles = getSampleStyleSheet()

    # Creating a custom justified paragraph style
    justified_style = ParagraphStyle(
        name='Justified',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
    )

    heading_style = ParagraphStyle(
        name='Heading',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=14,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6,
    )

    story = []

    # Add title if provided
    if title:
        title_style = ParagraphStyle(
            name='Title',
            parent=styles['Title'],
            fontName='Times-Bold',
            fontSize=18,
            leading=22,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=18,
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))

    # Split into paragraphs
    for para in text.strip().split('\n'):
        if para.strip():
            story.append(Paragraph(para.strip(), justified_style))
            story.append(Spacer(1, 12))  # 12 points = approx one line

    doc.build(story)

    # Move buffer pointer to beginning
    buffer.seek(0)
    return buffer