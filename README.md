# 🎯 AI Placement Copilot

A personal AI mentor for campus placements — built with **Streamlit**, **Gemini API**, **Python**, and **SQLite**.

## ✨ Features

- 📄 **Upload Resume** — parses PDF / DOCX / TXT
- 🎯 **ATS Score** — keyword-match score + Gemini recruiter-style feedback
- 🏢 **Company-wise Resume Suggestions** — tailored tips per target company
- 🗣️ **HR Interview Practice** — a live back-and-forth mock HR round
- 💻 **Technical Interview Questions** — by topic and difficulty, with model answers
- 🧮 **Aptitude Question Generator** — MCQs with answers and explanations
- 📊 **Skill Gap Analysis** — matched vs. missing skills for a target role
- 📅 **30-Day Learning Plan** — personalized, day-by-day
- ✉️ **Cover Letter Generator** — tailored to company + role
- 🔎 **Company Insights (bonus)** — e.g. *"I'm applying to TCS Digital"* →
  required skills, interview pattern, expected salary, FAQs (curated data
  for common recruiters + live Gemini lookup for anything else)

All ATS scores and AI-generated content (cover letters, plans, Q&A) are
logged to a local **SQLite** database (`placement_copilot.db`) so you can
build a history view later if you want.

The app works even **without** a Gemini API key — the ATS score falls back
to a transparent keyword-overlap calculation, and every AI page shows a
clear message asking you to add a key instead of crashing.

## 🗂️ Project structure

```
placement-copilot/
├── app.py                     # Streamlit app (entry point)
├── db.py                      # SQLite setup + helper functions
├── requirements.txt
├── .env.example                # copy to .env and add your key
├── utils/
│   ├── gemini_client.py       # Gemini API wrapper (graceful fallback)
│   ├── resume_parser.py       # PDF/DOCX/TXT text + skill extraction
│   ├── ats_scorer.py          # keyword-based + Gemini ATS scoring
│   └── company_data.py        # curated company profiles + Gemini fallback
└── README.md
```

## 🚀 Run locally

```bash
git clone https://github.com/<your-username>/ai-placement-copilot.git
cd ai-placement-copilot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# then open .env and paste your Gemini API key

streamlit run app.py
```

Get a free Gemini API key at **https://aistudio.google.com/app/apikey**.

### ⚠️ Important: don't run this with the "Run" button / `python app.py`

This is a **Streamlit** app, not a plain script. It must be started with:

```bash
streamlit run app.py
```

If you run it as `python app.py` (e.g. via VS Code's ▶️ Run button), it will
either crash or silently do nothing, because Streamlit needs its own server
process to render the UI in your browser.

### Windows tips

- Always `cd` into the `placement-copilot` folder first, then run
  `streamlit run app.py` from that same terminal/folder — don't run it via
  a full path from a temp/extracted-zip location.
- If `streamlit` isn't recognized, make sure your virtual environment is
  activated (`venv\Scripts\activate`) and re-run `pip install -r requirements.txt`.
- If you ever see an import error mentioning a file that isn't in this
  project, you likely have a **globally installed package with the same
  name** as one of this project's files, and Python is loading that instead.
  Run `pip show <package-name>` to confirm, then either uninstall it
  (`pip uninstall <package-name>`) or work inside a virtual environment
  (recommended) so global packages can't collide with project files.

## ☁️ Deploy on Streamlit Community Cloud (free)

1. Push this project to a **public GitHub repo**.
2. Go to **https://share.streamlit.io** and sign in with GitHub.
3. Click **"New app"**, pick your repo/branch, and set the main file to `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_actual_key_here"
   ```
5. Click **Deploy**. You'll get a public URL like
   `https://your-app-name.streamlit.app`.

> Note: Streamlit Community Cloud's filesystem is ephemeral — the SQLite
> file will reset on redeploys/restarts. For persistent history across
> restarts, swap `db.py` to a hosted database (e.g. Turso, Supabase Postgres)
> later; the function signatures are kept simple on purpose to make that
> swap easy.

## 🔒 Notes on the .env file

`.env` is already in `.gitignore` — **never commit your real API key**.
Only `.env.example` (with a placeholder) should be pushed to GitHub.

## 🛠️ Tech stack

| Layer      | Choice                          |
|------------|----------------------------------|
| UI         | Streamlit                        |
| AI         | Google Gemini API (`google-generativeai`) |
| Language   | Python 3.10+                     |
| Storage    | SQLite                           |
| Parsing    | pypdf, python-docx                |

## 📌 Ideas to extend

- Add login so `student_name` maps to a real account and history page.
- Add a "history" page reading from `db.get_history()` / `db.get_ats_history()`.
- Swap the keyword-based skill extraction in `resume_parser.py` for an
  embeddings-based similarity search for more accurate ATS scoring.
- Add PDF export for the cover letter and learning plan.
