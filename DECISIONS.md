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

## 4. Soft-Coding Remaining Sections & Ordering
- **Decision:** Introduce a `SiteContent` singleton model to hold global site variables (Hero text, About text, uploaded resume path) and add `display_order` fields to existing lists.
- **Rationale:** The user wants full dynamic control of all sections from the admin panel. Using a singleton table `SiteContent` is the simplest way to manage site-wide settings without complex multi-tenant or key-value setups. Adding an order integer column (`display_order`) is a simple, standard way to allow users to control the layout order of their projects, education, and experience.

## 5. Database Initialization Strategy (Render / Gunicorn)
- **Decision:** Move `db.create_all()` out of the module level in `app.py` and run `python seed.py` within `render.yaml` `startCommand` instead.
- **Rationale:** When running under Gunicorn (`gunicorn app:app`), the module-level `db.create_all()` was being executed before SQLAlchemy models were parsed and registered, causing empty tables (e.g. `relation "site_content" does not exist`). By removing it from `app.py` and prefixing the start command with `python seed.py`, the models are correctly imported before `db.create_all()` is called, and the initial data is immediately seeded before serving traffic.
