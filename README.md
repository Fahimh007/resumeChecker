# ATS Resume Checker

An intelligent Applicant Tracking System (ATS) Resume Checker built with Django. This application allows users to upload PDF resumes, compare them against specific job descriptions, and receive a comprehensive match analysis including scores, extracted skills, and experience details.

Live view: https://resume-checker-topaz-two.vercel.app/

## 🚀 Features

- **Resume Analysis**: Upload PDF resumes and analyze them against job descriptions.
- **Match Scoring**: Get an ATS compatibility score (%) estimating how well the resume matches the job requirements.
- **Skill Extraction**: Automatically identifies and lists skills found in the resume.
- **Project Categories & Experience**: Extracts project categories and years of experience.
- **Comparison Tool**: Select and compare multiple resume analyses side-by-side.
- **History Tracking**: Keeps a historic log of all analyzed resumes for later review or comparison.

## 🛠️ Technology Stack

- **Backend**: Python, Django, Django REST Framework
- **Frontend**: HTML, CSS, Bootstrap (for responsive design)
- **Database**: SQLite (default, easily swap to PostgreSQL/MySQL)

## ⚙️ Installation & Setup

Follow these steps to get your development environment set up:

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ats-checker.git
cd ats-checker
```

**2. Set up a Virtual Environment** (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies from the root directory**
```bash
pip install -r requirements.txt
```

**4. Run Database Migrations**
```bash
cd core
python manage.py migrate
```

**5. Start the Development Server**
```bash
python manage.py runserver
```
The application will now be running at `http://127.0.0.1:8000/`.

## 📖 Usage

1. Open the application in your browser.
2. Go to the "Job Descriptions" section to add a new Job Title and Description.
3. Navigate to "Analyze Resume", select the Job Description, and upload a candidate's PDF resume.
4. Review the generated detailed report to see the match score and extracted data.
5. Use the "History" and "Compare" tabs to view past analyses side-by-side.



