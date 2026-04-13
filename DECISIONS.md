# Architectural Decisions

## Status: FINALIZED

## 1. Backend Stack
- **Decision:** Python with Flask and SQLite.
- **Rationale:** The user wants a hidden admin portal, dynamic data management, and AI integration for parsing resumes. Flask is lightweight, easy to set up for a simple portfolio site, and Python has excellent support for AI API integrations (like the Google Gemini SDK). SQLite is chosen as the database because it is file-based and requires zero external setup, perfect for a personal portfolio.

## 2. Frontend Structure
- **Decision:** Separate existing single `index.html` into `templates/index.html` (Jinja), `static/css/style.css`, and `static/js/script.js`.
- **Rationale:** Improves maintainability. The current UI/UX (Tailwind + Vanilla JS + Vanilla CSS) will be fully preserved, just reorganized. Assets will be moved to `static/assets/`.

## 3. AI Resume Parsing
- **Decision:** Use Gemini API to extract structured JSON data from uploaded resumes.
- **Rationale:** Automates the process of updating skills and experiences in the portfolio. The extracted data shape is explicitly defined in `SPEC.md` to ensure predictable database insertions.
