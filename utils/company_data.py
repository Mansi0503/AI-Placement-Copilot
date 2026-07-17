"""Static knowledge base for common campus-placement recruiters, plus a
Gemini-powered fallback for any company/role not covered here.

This directly powers the bonus feature:
  "I'm applying to TCS Digital." -> required skills, interview pattern,
  expected salary, FAQs.
"""

from utils import gemini_client

COMPANY_KB = {
    "tcs digital": {
        "skills": ["Data Structures", "SQL", "OOP concepts", "Aptitude",
                    "Communication", "Basic Web Dev", "Any one programming language"],
        "pattern": [
            "Round 1: NQT (National Qualifier Test) - Verbal, Reasoning, Quant, Coding",
            "Round 2: Technical Interview - CS fundamentals, projects, coding",
            "Round 3: Managerial/HR Interview",
        ],
        "salary": "₹7 – 9 LPA (higher than TCS Ninja/Prime)",
        "faqs": [
            "Why TCS Digital and not TCS Ninja?",
            "Explain your final year project in depth.",
            "Difference between SQL and NoSQL.",
            "OOP concepts with real examples.",
            "Puzzle-based aptitude questions.",
        ],
    },
    "infosys": {
        "skills": ["Aptitude", "Pseudocode", "DBMS", "OOPs", "Communication"],
        "pattern": [
            "Round 1: Online Test - Aptitude, Pseudocode, Puzzle solving",
            "Round 2: Technical Interview",
            "Round 3: HR Interview",
        ],
        "salary": "₹3.6 – 9 LPA depending on offer (SP/Digital Specialist/Power Programmer)",
        "faqs": [
            "Tell me about yourself.",
            "Explain a project from your resume.",
            "What is normalization in DBMS?",
            "Basic OOP pillars with examples.",
        ],
    },
    "wipro": {
        "skills": ["Aptitude", "Verbal Ability", "Coding basics", "Communication"],
        "pattern": [
            "Round 1: WILP/NLTH Online Test - Aptitude, Verbal, Coding",
            "Round 2: Technical + HR Interview (often combined)",
        ],
        "salary": "₹3.5 – 6.5 LPA",
        "faqs": [
            "Why do you want to join Wipro?",
            "Explain your academic project.",
            "Basic questions on your strongest programming language.",
        ],
    },
    "accenture": {
        "skills": ["Aptitude", "Communication", "Basic coding", "Cognitive ability"],
        "pattern": [
            "Round 1: Cognitive & Technical Assessment",
            "Round 2: Coding Assessment (for tech roles)",
            "Round 3: HR/Communication Interview",
        ],
        "salary": "₹4.5 – 6.5 LPA",
        "faqs": [
            "Tell me about a time you solved a difficult problem.",
            "Why Accenture?",
            "Basic project walkthrough.",
        ],
    },
    "cognizant": {
        "skills": ["Aptitude", "Coding (GenC Next/Elevate tracks)", "Communication"],
        "pattern": [
            "Round 1: AMCAT-based Online Test",
            "Round 2: Technical Interview",
            "Round 3: HR Interview",
        ],
        "salary": "₹4 – 6.5 LPA (GenC Next pays more)",
        "faqs": [
            "Explain OOP concepts.",
            "Walk through your resume project.",
            "Why Cognizant?",
        ],
    },
    "capgemini": {
        "skills": ["Aptitude", "Pseudocode", "English communication", "Group discussion"],
        "pattern": [
            "Round 1: Aptitude + Pseudocode + Communication Test",
            "Round 2: Group Discussion (sometimes)",
            "Round 3: Technical + HR Interview",
        ],
        "salary": "₹4 – 7.6 LPA",
        "faqs": [
            "Tell me about yourself.",
            "Explain your project.",
            "Basic pseudocode questions.",
        ],
    },
    "amazon": {
        "skills": ["Data Structures & Algorithms", "System Design (basic)",
                    "Leadership Principles", "Problem solving"],
        "pattern": [
            "Round 1: Online Assessment - DSA + Leadership Principles MCQs",
            "Round 2-3: Technical Interviews (DSA, CS fundamentals)",
            "Round 4: Bar Raiser / Leadership Principles Interview",
        ],
        "salary": "₹12 – 20+ LPA (varies significantly by role/level)",
        "faqs": [
            "Tell me about a time you disagreed with your manager.",
            "Solve a DSA problem on arrays/trees/graphs.",
            "Which Amazon Leadership Principle resonates with you most?",
        ],
    },
    "deloitte": {
        "skills": ["Aptitude", "Communication", "Case study analysis", "Excel basics"],
        "pattern": [
            "Round 1: Online Aptitude + Written Communication Test",
            "Round 2: Group Discussion / Case Study",
            "Round 3: HR + Technical Interview",
        ],
        "salary": "₹4.5 – 7 LPA",
        "faqs": [
            "Tell me about yourself.",
            "Case study: how would you approach this business problem?",
            "Why consulting?",
        ],
    },
}


def get_company_info(company_name: str) -> dict:
    """Look up a company in the static KB; otherwise ask Gemini to generate
    a similarly-structured profile."""
    key = company_name.strip().lower()

    if key in COMPANY_KB:
        info = dict(COMPANY_KB[key])
        info["source"] = "curated"
        return info

    # Fallback: ask Gemini for a best-effort structured profile
    if not gemini_client.is_configured():
        return {
            "skills": [],
            "pattern": [],
            "salary": "Not available offline.",
            "faqs": [],
            "source": "unavailable",
            "note": (
                f"'{company_name}' isn't in the built-in database yet, and no Gemini "
                "API key is configured to fetch it live. Add a key to unlock this."
            ),
        }

    prompt = f"""
Give a campus-placement profile for freshers applying to "{company_name}".
Respond ONLY in this exact plain-text format (no markdown, no extra commentary):

SKILLS: skill1, skill2, skill3, ...
PATTERN: Round 1 description | Round 2 description | Round 3 description
SALARY: expected CTC range for freshers in India
FAQS: question1 | question2 | question3
"""
    raw = gemini_client.generate(prompt, temperature=0.4)

    info = {"skills": [], "pattern": [], "salary": "Not available.", "faqs": [],
            "source": "gemini"}
    try:
        for line in raw.splitlines():
            if line.upper().startswith("SKILLS:"):
                info["skills"] = [s.strip() for s in line.split(":", 1)[1].split(",") if s.strip()]
            elif line.upper().startswith("PATTERN:"):
                info["pattern"] = [s.strip() for s in line.split(":", 1)[1].split("|") if s.strip()]
            elif line.upper().startswith("SALARY:"):
                info["salary"] = line.split(":", 1)[1].strip()
            elif line.upper().startswith("FAQS:"):
                info["faqs"] = [s.strip() for s in line.split(":", 1)[1].split("|") if s.strip()]
    except Exception:
        info["note"] = raw  # show raw response if parsing fails

    return info


def list_known_companies():
    return sorted(k.title() for k in COMPANY_KB.keys())
