<div align="center">

# 🚀 AI Placement Copilot

### *An AI-Powered Career Preparation Platform for Students & Job Seekers*

Transform your placement journey with **AI-driven resume analysis, ATS optimization, interview preparation, and personalized career guidance**—all in one intelligent web application.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

⭐ If you like this project, consider giving it a star!

</div>

---

# 📖 Overview

Preparing for placements often requires using multiple platforms for resume reviews, ATS checks, interview preparation, and career planning.

**AI Placement Copilot** brings all these essential tools together into a single AI-powered platform.

Built using **Python**, **Streamlit**, **Google Gemini AI**, and **SQLite**, this application helps students improve their resumes, practice interviews, identify skill gaps, and receive personalized learning recommendations.

Whether you're applying for internships, campus placements, or full-time software roles, AI Placement Copilot acts as your personal AI career assistant.

---

# 🎯 Problem Statement

Many students struggle with:

- Low ATS resume scores
- Generic resumes
- Lack of interview preparation
- Difficulty identifying skill gaps
- No personalized career guidance

This project solves these challenges using Generative AI.

---

# 💡 Key Features

## 📄 AI Resume Analyzer

✔ Upload resumes in PDF or DOCX format

✔ Automatically extract resume details

✔ AI-generated resume review

✔ Actionable improvement suggestions

---

## 🎯 ATS Resume Score

Evaluate resume compatibility with Applicant Tracking Systems.

Features include:

- ATS Score
- Keyword Matching
- Missing Skills Detection
- Resume Optimization Suggestions
- Recruiter-Friendly Formatting Tips

---

## 🏢 Company-Specific Resume Optimization

Generate tailored resume recommendations for companies such as:

- Google
- Microsoft
- Amazon
- Deloitte
- Accenture
- Infosys
- TCS
- Capgemini
- Cognizant
- Wipro

---

## 🤖 AI Interview Preparation

Practice with AI-generated interview questions.

Includes:

- HR Questions
- Technical Questions
- Behavioral Questions
- Follow-up Questions
- AI Feedback

---

## 📊 Skill Gap Analysis

Identify missing skills required for your target role.

The application suggests:

- Technical Skills
- Soft Skills
- Certifications
- Courses
- Learning Priorities

---

## 📚 Personalized Learning Roadmap

Generate customized study plans based on:

- Current Skill Set
- Career Goal
- Experience Level
- Missing Skills

---

## 💾 Resume Database

Store and manage resume analysis history using SQLite.

---

# 🏗️ System Architecture

```
               Resume Upload
                      │
                      ▼
            Resume Parsing Module
                      │
                      ▼
             Google Gemini AI
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 ATS Analysis   Interview Module   Skill Analysis
      │               │                │
      └───────────────┼────────────────┘
                      ▼
          Personalized Recommendations
                      │
                      ▼
            Streamlit User Interface
                      │
                      ▼
                SQLite Database
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Artificial Intelligence | Google Gemini API |
| Database | SQLite |
| Resume Parsing | PyPDF2, python-docx |
| Data Processing | Pandas, NumPy |
| Environment Management | python-dotenv |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```
AI-Placement-Copilot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── copilot_db.py
│
├── utils/
│   ├── ats_scorer.py
│   ├── company_data.py
│   ├── gemini_client.py
│   └── resume_parser.py
│
├── assets/
│
└── screenshots/
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/YourUsername/AI-Placement-Copilot.git
```

Move into the project directory.

```bash
cd AI-Placement-Copilot
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application.

```bash
streamlit run app.py
```

---

# 🖥️ Application Modules

- Home Dashboard
- Resume Upload
- ATS Resume Analyzer
- Resume Optimization
- Company Resume Analysis
- AI Interview Practice
- Skill Gap Analysis
- Learning Roadmap
- Resume History

---

# 📸 Screenshots

> Add screenshots after deployment.

| Dashboard | ATS Analysis |
|-----------|--------------|
| *(Screenshot)* | *(Screenshot)* |

| Interview Practice | Learning Roadmap |
|-------------------|------------------|
| *(Screenshot)* | *(Screenshot)* |

---

# 🎯 Use Cases

- Campus Placements
- Internship Applications
- Resume Building
- Career Guidance
- AI Interview Practice
- Software Engineering Roles
- Data Science & AI/ML Roles

---

# 📈 Future Scope

- LinkedIn Profile Analyzer
- Resume Builder
- Job Recommendation System
- AI Career Mentor
- Voice-Based Mock Interviews
- Resume Version Comparison
- Multi-language Support
- Cloud Deployment

---

# 🧠 Skills Demonstrated

This project demonstrates practical knowledge of:

- Python Development
- Generative AI Integration
- Prompt Engineering
- Streamlit Web Application Development
- Resume Parsing
- ATS Resume Evaluation
- SQLite Database Design
- Modular Software Architecture
- Git & GitHub Workflow
- API Integration
- User Interface Design

---

# 📊 Project Highlights

- AI-powered career preparation platform
- Intelligent ATS resume scoring
- Google Gemini AI integration
- Personalized interview preparation
- Company-specific resume optimization
- Dynamic learning roadmap generation
- Interactive Streamlit interface
- Clean modular architecture
- Lightweight SQLite database
- Resume-ready portfolio project

---

# 👩‍💻 Author

## Mansi Verma

**B.Tech – Computer Science Engineering (Artificial Intelligence & Machine Learning)**

VIT Bhopal University

📧 Email: mv699205@gmail.com

---

<div align="center">

### ⭐ If this project helped you, please consider giving it a Star!

**Made with ❤️ using Python, Streamlit & Google Gemini AI**

</div>
