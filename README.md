# AI Resume Analyzer

A Streamlit web-based application that utilizes the OpenAI API to analyze your resume personalized to the job title or description provided, helping you find strengths and areas of improvement. The AI generates an in-depth analysis report which can be downloaded.

## Features

- **Upload Resume**: Upload your resume as a PDF file
- **Job Matching**: Paste a job title or full job description for personalized analysis
- **Resume Extraction**: Automatically extract name, email, phone number, skills, and experience from the resume
- **Smart Comparison**: Compare your resume against job requirements using AI
- **AI-Powered Feedback**: Get detailed feedback using OpenAI's language models
- **Cover Letter Generation**: Generate a personalized cover letter based on your resume and job description
- **Vagueness Report**: Receive suggestions to improve unclear or vague sections of your resume
- **Downloadable Reports**: Export analysis results as PDF reports

## How It Works

1. **Text Extraction**: Extracts resume text using `PyMuPDF` for accurate PDF parsing
2. **AI Analysis**: Uses keyword matching and OpenAI with tailored prompts to assess the resume
3. **Job Comparison**: Intelligently compares your resume with the provided job description
4. **User Interface**: Displays comprehensive analysis in a user-friendly Streamlit interface

## Technologies Used

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **OpenAI API** - AI-powered text analysis and generation
- **PyMuPDF** - PDF text extraction
- **python-dotenv** - Environment variable management for API keys

## Prerequisites

- Python 3.7 or higher
- OpenAI API key (requires $5 credit minimum)
- Git (for cloning the repository)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Install Dependencies

```bash
pip install streamlit openai PyMuPDF python-dotenv
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Application

For **Streamlit Web Interface** (Recommended):
```bash
streamlit run app.py
```

For **Console Interface** (Local Testing):
```bash
python UI/main.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

## Usage

1. **Upload Resume**: Click the upload button and select your PDF resume
2. **Enter Job Details**: Paste the job title or complete job description in the text area
3. **Analyze**: Click the analyze button to generate your personalized report
4. **Review Results**: View the comprehensive analysis including:
   - Resume strengths and weaknesses
   - Job match percentage
   - Improvement suggestions
   - Generated cover letter
5. **Download Report**: Export your analysis as a PDF for future reference

## Configuration for Local Development

If you want to run the project locally with console output, make the following changes:

### In `pdftools.py`:

**Remove these lines from `extract_text_from_pdf` function:**
```python
file_bytes = uploaded_file.read()
doc = fitz.open(stream=file_bytes, filetype="pdf")
```

**Uncomment this line:**
```python
doc = fitz.open(uploaded_file)
```

**For PDF report generation:**
- Uncomment the `generate_pdf` function to save analysis reports as PDF locally
- Comment out the `generate_pdf_buffer` function

## API Costs

- **OpenAI API Key**: Requires minimum $5 credit purchase
- **Recommended Model**: GPT-4.1-nano (most cost-effective option)
- **Cost per Analysis**: Approximately >$0.01 per resume analysis


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This application requires an active internet connection for OpenAI API calls. Ensure you have sufficient API credits before running extensive analyses.
