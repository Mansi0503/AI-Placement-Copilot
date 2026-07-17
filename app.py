"""AI Placement Copilot — a personal AI mentor for campus placements.

Run locally:
    streamlit run app.py

Deploy on Streamlit Community Cloud (free) pointed at your GitHub repo,
then add GEMINI_API_KEY under App -> Settings -> Secrets.
"""

import streamlit as st

import copilot_db as db
from utils import gemini_client, resume_parser, ats_scorer, company_data

# --------------------------------------------------------------------------
# App setup
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Placement Copilot",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_id" not in st.session_state:
    st.session_state.resume_id = None
if "student_name" not in st.session_state:
    st.session_state.student_name = "Guest"
if "hr_chat" not in st.session_state:
    st.session_state.hr_chat = []

PAGES = [
    "🏠 Home",
    "📄 Upload Resume",
    "🎯 ATS Score",
    "🏢 Company-wise Suggestions",
    "🗣️ HR Interview Practice",
    "💻 Technical Interview Questions",
    "🧮 Aptitude Question Generator",
    "📊 Skill Gap Analysis",
    "📅 30-Day Learning Plan",
    "✉️ Cover Letter Generator",
    "🔎 Company Insights",
]

with st.sidebar:
    st.title("🎯 Placement Copilot")
    st.session_state.student_name = st.text_input(
        "Your name", value=st.session_state.student_name
    )
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")

    st.markdown("---")
    if gemini_client.is_configured():
        st.success("Gemini API: connected")
    else:
        st.warning("Gemini API: not configured\n\nAdd GEMINI_API_KEY to `.env` "
                    "or Streamlit secrets to unlock AI features.")

    if st.session_state.resume_text:
        st.caption(f"Resume loaded: {len(st.session_state.resume_text)} characters")
    else:
        st.caption("No resume uploaded yet.")


def require_resume():
    if not st.session_state.resume_text:
        st.info("Upload your resume first on the **📄 Upload Resume** page.")
        st.stop()


# --------------------------------------------------------------------------
# 🏠 Home
# --------------------------------------------------------------------------
if page == "🏠 Home":
    st.title("🎯 AI Placement Copilot")
    st.subheader("Your personal AI mentor for placements")
    st.write(
        "Upload your resume once, then use any of the tools in the sidebar — "
        "ATS scoring, company-specific resume tips, mock HR/technical interviews, "
        "aptitude practice, skill-gap analysis, a 30-day learning plan, and cover "
        "letter generation."
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Features", "9 tools")
    with col2:
        st.metric("Powered by", "Gemini API")
    with col3:
        st.metric("Storage", "SQLite (local)")

    st.markdown("### Quick start")
    st.markdown(
        "1. Go to **📄 Upload Resume** and upload a PDF/DOCX/TXT file.\n"
        "2. Try **🎯 ATS Score** against a job description.\n"
        "3. Ask **🔎 Company Insights** something like *\"TCS Digital\"* "
        "for required skills, interview pattern, salary, and FAQs."
    )

# --------------------------------------------------------------------------
# 📄 Upload Resume
# --------------------------------------------------------------------------
elif page == "📄 Upload Resume":
    st.title("📄 Upload Resume")
    uploaded = st.file_uploader("Upload your resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

    if uploaded is not None:
        try:
            text = resume_parser.extract_text(uploaded)
            st.session_state.resume_text = text
            resume_id = db.save_resume(st.session_state.student_name, uploaded.name, text)
            st.session_state.resume_id = resume_id
            st.success(f"Parsed {uploaded.name} — {len(text)} characters extracted.")
        except Exception as e:
            st.error(f"Couldn't read that file: {e}")

    if st.session_state.resume_text:
        with st.expander("Preview extracted text"):
            st.text(st.session_state.resume_text[:4000])

        skills = resume_parser.extract_skills(st.session_state.resume_text)
        st.markdown("**Detected skills:**")
        st.write(", ".join(skills) if skills else "No common skills detected — try a plain-text export of your resume.")

# --------------------------------------------------------------------------
# 🎯 ATS Score
# --------------------------------------------------------------------------
elif page == "🎯 ATS Score":
    st.title("🎯 ATS Score")
    require_resume()

    jd_text = st.text_area("Paste the job description", height=200,
                            placeholder="Paste the job description you're targeting here...")
    target_company = st.text_input("Target company (optional, for your history log)")

    if st.button("Calculate ATS Score", type="primary") and jd_text.strip():
        score, matched, missing = ats_scorer.keyword_ats_score(st.session_state.resume_text, jd_text)

        st.markdown(f"### Score: **{score}%**")
        st.progress(min(int(score), 100) / 100)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Matched keywords**")
            st.write(", ".join(matched) if matched else "—")
        with col2:
            st.markdown("**❌ Missing keywords**")
            st.write(", ".join(missing) if missing else "—")

        with st.spinner("Getting recruiter-style feedback from Gemini..."):
            feedback = ats_scorer.gemini_ats_feedback(st.session_state.resume_text, jd_text)
        st.markdown("**📝 Detailed feedback**")
        st.write(feedback)

        if st.session_state.resume_id:
            db.save_ats_score(st.session_state.resume_id, target_company, score, matched, missing, feedback)

# --------------------------------------------------------------------------
# 🏢 Company-wise Resume Suggestions
# --------------------------------------------------------------------------
elif page == "🏢 Company-wise Suggestions":
    st.title("🏢 Company-wise Resume Suggestions")
    require_resume()

    company = st.text_input("Which company are you tailoring your resume for?", placeholder="e.g. TCS Digital, Amazon, Infosys")
    role = st.text_input("Role (optional)", placeholder="e.g. Software Engineer, Data Analyst")

    if st.button("Get Suggestions", type="primary") and company.strip():
        prompt = f"""
A student is tailoring their resume for {company} {f'for the role of {role}' if role else ''}.

RESUME:
\"\"\"{st.session_state.resume_text[:6000]}\"\"\"

Give 5-7 specific, actionable suggestions to tailor this resume for {company}.
Focus on: keywords to add, sections to reorder/emphasize, and quantifiable
achievements to highlight. Use a short bulleted list.
"""
        with st.spinner(f"Analyzing resume for {company}..."):
            suggestions = gemini_client.generate(prompt, temperature=0.5)
        st.markdown(suggestions)
        db.save_generated_content(st.session_state.student_name, "resume_suggestions", company, suggestions)

# --------------------------------------------------------------------------
# 🗣️ HR Interview Practice
# --------------------------------------------------------------------------
elif page == "🗣️ HR Interview Practice":
    st.title("🗣️ HR Interview Practice")
    require_resume()
    st.caption("A simulated HR round. The AI asks a question, you answer, it gives feedback and asks the next one.")

    for msg in st.session_state.hr_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if st.button("Start / Ask next question"):
        history_text = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.hr_chat[-6:])
        prompt = f"""
You are a friendly but thorough HR interviewer for a fresher/campus placement.
Candidate's resume summary:
\"\"\"{st.session_state.resume_text[:3000]}\"\"\"

Conversation so far:
{history_text if history_text else "(interview just starting)"}

If the conversation just started, ask a warm opening HR question (e.g. "Tell me about yourself").
Otherwise, briefly (1-2 sentences) give constructive feedback on the candidate's last answer,
then ask exactly ONE new HR interview question. Keep your whole reply under 80 words.
"""
        question = gemini_client.generate(prompt, temperature=0.7)
        st.session_state.hr_chat.append({"role": "assistant", "content": question})
        st.rerun()

    user_answer = st.chat_input("Type your answer...")
    if user_answer:
        st.session_state.hr_chat.append({"role": "user", "content": user_answer})
        st.rerun()

    if st.button("Clear conversation"):
        st.session_state.hr_chat = []
        st.rerun()

# --------------------------------------------------------------------------
# 💻 Technical Interview Questions
# --------------------------------------------------------------------------
elif page == "💻 Technical Interview Questions":
    st.title("💻 Technical Interview Questions")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.selectbox("Topic", ["Python", "Java", "SQL/DBMS", "Data Structures & Algorithms",
                                        "Machine Learning", "Computer Networks", "Operating Systems",
                                        "Web Development", "OOP Concepts"])
    with col2:
        difficulty = st.select_slider("Difficulty", ["Beginner", "Intermediate", "Advanced"])

    num_q = st.slider("Number of questions", 3, 10, 5)

    if st.button("Generate Questions", type="primary"):
        resume_context = f"\nCandidate's resume:\n\"\"\"{st.session_state.resume_text[:2000]}\"\"\"" if st.session_state.resume_text else ""
        prompt = f"""
Generate {num_q} {difficulty.lower()}-level technical interview questions on {topic}
for a campus placement / fresher interview.{resume_context}

For each question, also give a concise model answer (2-4 sentences).
Format clearly as:
Q1: ...
A1: ...
"""
        with st.spinner(f"Generating {num_q} {topic} questions..."):
            content = gemini_client.generate(prompt, temperature=0.6)
        st.markdown(content)
        db.save_generated_content(st.session_state.student_name, "technical_questions", topic, content)

# --------------------------------------------------------------------------
# 🧮 Aptitude Question Generator
# --------------------------------------------------------------------------
elif page == "🧮 Aptitude Question Generator":
    st.title("🧮 Aptitude Question Generator")

    category = st.selectbox("Category", ["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability", "Data Interpretation"])
    num_q = st.slider("Number of questions", 3, 10, 5, key="apt_num")

    if st.button("Generate Aptitude Questions", type="primary"):
        prompt = f"""
Generate {num_q} multiple-choice {category} questions typical of campus placement
aptitude tests (like TCS NQT, Infosys, Wipro etc).

For each question give 4 options (A-D), then clearly mark the correct answer
and a one-line explanation. Format as:
Q1: ...
A) ... B) ... C) ... D) ...
Answer: ...
Explanation: ...
"""
        with st.spinner(f"Generating {category} questions..."):
            content = gemini_client.generate(prompt, temperature=0.6)
        st.markdown(content)
        db.save_generated_content(st.session_state.student_name, "aptitude_questions", category, content)

# --------------------------------------------------------------------------
# 📊 Skill Gap Analysis
# --------------------------------------------------------------------------
elif page == "📊 Skill Gap Analysis":
    st.title("📊 Skill Gap Analysis")
    require_resume()

    target_role = st.text_input("Target role", placeholder="e.g. Data Analyst, Backend Developer, ML Engineer")

    if st.button("Analyze Skill Gap", type="primary") and target_role.strip():
        current_skills = resume_parser.extract_skills(st.session_state.resume_text)

        prompt = f"""
A student wants to become a "{target_role}". Their currently detected skills are:
{', '.join(current_skills) if current_skills else 'none clearly detected'}

Full resume for context:
\"\"\"{st.session_state.resume_text[:4000]}\"\"\"

List:
1. MATCHED SKILLS: skills they already have that are relevant
2. MISSING SKILLS: important skills for this role they don't yet have
3. RECOMMENDED RESOURCES: 3-5 specific free/low-cost resources (courses, docs, platforms) to close the gap

Keep it concise and use headers exactly as: Matched Skills / Missing Skills / Recommended Resources
"""
        with st.spinner(f"Analyzing gap for {target_role}..."):
            content = gemini_client.generate(prompt, temperature=0.5)
        st.markdown(content)
        db.save_generated_content(st.session_state.student_name, "skill_gap", target_role, content)

# --------------------------------------------------------------------------
# 📅 30-Day Learning Plan
# --------------------------------------------------------------------------
elif page == "📅 30-Day Learning Plan":
    st.title("📅 30-Day Learning Plan")
    require_resume()

    target_role = st.text_input("Goal / target role", placeholder="e.g. crack SDE interviews, become job-ready as a Data Analyst")
    hours_per_day = st.slider("Hours available per day", 1, 8, 3)

    if st.button("Generate 30-Day Plan", type="primary") and target_role.strip():
        prompt = f"""
Create a 30-day, day-by-day learning plan for a student aiming to: "{target_role}".
They have about {hours_per_day} hours/day available.

Resume for context (skills they already have):
\"\"\"{st.session_state.resume_text[:3000]}\"\"\"

Group the plan into 4 weekly blocks (Week 1-4) with a short goal for each week,
then a compact day-by-day breakdown (Day 1, Day 2, ...) with specific topics/tasks.
Keep each day's entry to one line.
"""
        with st.spinner("Building your 30-day plan..."):
            plan = gemini_client.generate(prompt, temperature=0.6)
        st.markdown(plan)
        db.save_generated_content(st.session_state.student_name, "learning_plan", target_role, plan)

        st.download_button("Download plan as .txt", plan, file_name="30_day_learning_plan.txt")

# --------------------------------------------------------------------------
# ✉️ Cover Letter Generator
# --------------------------------------------------------------------------
elif page == "✉️ Cover Letter Generator":
    st.title("✉️ Cover Letter Generator")
    require_resume()

    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company")
        role = st.text_input("Role applying for")
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Enthusiastic", "Concise", "Formal"])

    jd_text = st.text_area("Job description (optional, improves relevance)", height=120)

    if st.button("Generate Cover Letter", type="primary") and company.strip() and role.strip():
        prompt = f"""
Write a {tone.lower()} cover letter for a fresher/student applying to {company}
for the role of {role}.

Resume:
\"\"\"{st.session_state.resume_text[:4000]}\"\"\"

{"Job description: " + jd_text[:2000] if jd_text.strip() else ""}

Keep it to 250-300 words, 3-4 paragraphs, and highlight specific projects/skills
from the resume rather than generic statements. Do not invent facts not present
in the resume.
"""
        with st.spinner("Writing your cover letter..."):
            letter = gemini_client.generate(prompt, temperature=0.6)
        st.markdown(letter)
        db.save_generated_content(st.session_state.student_name, "cover_letter", f"{company} - {role}", letter)
        st.download_button("Download as .txt", letter, file_name=f"cover_letter_{company}.txt")

# --------------------------------------------------------------------------
# 🔎 Company Insights  (bonus feature)
# --------------------------------------------------------------------------
elif page == "🔎 Company Insights":
    st.title("🔎 Company Insights")
    st.caption('Ask something like "I\'m applying to TCS Digital" or just type a company name.')

    known = company_data.list_known_companies()
    st.caption(f"Built-in profiles: {', '.join(known)} — anything else is fetched live via Gemini.")

    query = st.text_input("Company (or a sentence mentioning one)", placeholder="I'm applying to TCS Digital")

    if st.button("Get Insights", type="primary") and query.strip():
        # crude extraction: strip common filler phrases, otherwise pass whole query
        cleaned = query.lower()
        for phrase in ["i'm applying to", "i am applying to", "applying to", "i want to join"]:
            cleaned = cleaned.replace(phrase, "")
        cleaned = cleaned.strip(" .!") or query

        with st.spinner(f"Looking up {cleaned.title()}..."):
            info = company_data.get_company_info(cleaned)

        st.subheader(cleaned.title())

        if info.get("note"):
            st.info(info["note"])

        st.markdown("**Required skills**")
        st.write(", ".join(info["skills"]) if info["skills"] else "—")

        st.markdown("**Interview pattern**")
        for i, step in enumerate(info["pattern"], 1):
            st.write(f"{i}. {step}")

        st.markdown("**Expected salary (freshers, India)**")
        st.write(info["salary"])

        st.markdown("**Frequently asked questions**")
        for q in info["faqs"]:
            st.write(f"- {q}")

        st.caption(f"Source: {'curated database' if info['source'] == 'curated' else 'Gemini (live)'}")
