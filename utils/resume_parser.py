"""Extract raw text from an uploaded resume file (PDF / DOCX / TXT)."""

import io
from pypdf import PdfReader
from docx import Document


def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    data = uploaded_file.read()

    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(data))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text.strip()

    if name.endswith(".docx"):
        doc = Document(io.BytesIO(data))
        text = "\n".join(p.text for p in doc.paragraphs)
        return text.strip()

    if name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore").strip()

    raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")


# A small, dependency-free skill vocabulary used across the app for
# quick keyword-based matching (ATS score, skill gap analysis, etc).
COMMON_SKILLS = [
    "python", "java", "c++", "c", "javascript", "typescript", "sql", "nosql",
    "html", "css", "react", "angular", "vue", "node.js", "flask", "django",
    "fastapi", "spring boot", "machine learning", "deep learning",
    "data structures", "algorithms", "dbms", "operating systems",
    "computer networks", "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "opencv", "nlp", "computer vision", "power bi",
    "tableau", "excel", "aws", "azure", "gcp", "docker", "kubernetes",
    "git", "github", "linux", "rest api", "microservices", "agile",
    "data analysis", "data science", "statistics", "communication",
    "leadership", "teamwork", "problem solving",
]


def extract_skills(text: str) -> list:
    """Naive keyword-based skill extraction against COMMON_SKILLS."""
    text_lower = text.lower()
    return sorted({skill for skill in COMMON_SKILLS if skill in text_lower})
