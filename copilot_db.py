"""SQLite storage layer for AI Placement Copilot.

Keeps a lightweight local history of resumes, ATS scores, and anything the
AI generates (cover letters, learning plans, interview Q&A) so a student can
look back at previous sessions.
"""

import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "placement_copilot.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            file_name TEXT,
            resume_text TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ats_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            target_company TEXT,
            score REAL,
            matched_keywords TEXT,
            missing_keywords TEXT,
            feedback TEXT,
            created_at TEXT,
            FOREIGN KEY(resume_id) REFERENCES resumes(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS generated_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            content_type TEXT,
            title TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_resume(student_name, file_name, resume_text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO resumes (student_name, file_name, resume_text, created_at) VALUES (?, ?, ?, ?)",
        (student_name, file_name, resume_text, datetime.datetime.now().isoformat()),
    )
    conn.commit()
    resume_id = cur.lastrowid
    conn.close()
    return resume_id


def save_ats_score(resume_id, target_company, score, matched, missing, feedback):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO ats_scores
           (resume_id, target_company, score, matched_keywords, missing_keywords, feedback, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            resume_id,
            target_company,
            score,
            ", ".join(matched),
            ", ".join(missing),
            feedback,
            datetime.datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def save_generated_content(student_name, content_type, title, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO generated_content (student_name, content_type, title, content, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (student_name, content_type, title, content, datetime.datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_history(student_name, content_type=None, limit=20):
    conn = get_connection()
    cur = conn.cursor()
    if content_type:
        cur.execute(
            """SELECT * FROM generated_content WHERE student_name = ? AND content_type = ?
               ORDER BY created_at DESC LIMIT ?""",
            (student_name, content_type, limit),
        )
    else:
        cur.execute(
            """SELECT * FROM generated_content WHERE student_name = ?
               ORDER BY created_at DESC LIMIT ?""",
            (student_name, limit),
        )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_ats_history(student_name, limit=20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT ats_scores.*, resumes.student_name FROM ats_scores
           JOIN resumes ON ats_scores.resume_id = resumes.id
           WHERE resumes.student_name = ?
           ORDER BY ats_scores.created_at DESC LIMIT ?""",
        (student_name, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return rows
