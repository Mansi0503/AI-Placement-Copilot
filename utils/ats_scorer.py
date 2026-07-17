"""ATS (Applicant Tracking System) scoring.

Combines a transparent keyword-overlap score (works with zero API calls)
with an optional richer Gemini review for qualitative feedback.
"""

import re
from collections import Counter
from utils import gemini_client

STOPWORDS = set("""
a an the and or but if while of to in on for with as at by from is are was
were be been being this that these those it its it's you your we our they
their he she his her will would can could should must shall not no do does
did have has had i me my mine ours yours theirs him them who whom which
into over under above below out up down between during before after about
than then so such more most other some any all each every both few less
least own same too very just
""".split())


def _tokenize(text: str) -> list:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+.#]{1,}", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def keyword_ats_score(resume_text: str, jd_text: str, top_n: int = 25):
    """Rule-based score: overlap between the most frequent JD terms and the resume."""
    jd_tokens = _tokenize(jd_text)
    resume_tokens = set(_tokenize(resume_text))

    jd_keyword_freq = Counter(jd_tokens)
    top_keywords = [w for w, _ in jd_keyword_freq.most_common(top_n)]

    if not top_keywords:
        return 0.0, [], []

    matched = [kw for kw in top_keywords if kw in resume_tokens]
    missing = [kw for kw in top_keywords if kw not in resume_tokens]

    score = round((len(matched) / len(top_keywords)) * 100, 1)
    return score, matched, missing


def gemini_ats_feedback(resume_text: str, jd_text: str) -> str:
    """Ask Gemini for qualitative, recruiter-style feedback on the resume."""
    if not gemini_client.is_configured():
        return (
            "Add a Gemini API key to unlock detailed, recruiter-style feedback "
            "(formatting, impact statements, quantified achievements, etc.)."
        )

    prompt = f"""
You are an experienced technical recruiter reviewing a resume against a job description
for ATS (Applicant Tracking System) compatibility.

RESUME:
\"\"\"{resume_text[:6000]}\"\"\"

JOB DESCRIPTION:
\"\"\"{jd_text[:3000]}\"\"\"

Give concise, actionable feedback as a short bulleted list covering:
1. Missing but important keywords/skills
2. Formatting or structure issues that could confuse an ATS parser
3. 2-3 concrete rewrite suggestions for weak or vague bullet points
Keep the whole response under 200 words.
"""
    return gemini_client.generate(prompt, temperature=0.4)
