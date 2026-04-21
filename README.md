# AI-Powered Dynamic Portfolio

A dynamic, customizable personal portfolio website built with Python (Flask) featuring an integrated **AI Resume Parser**. Instead of manually typing out all your past jobs and skills, simply upload a PDF of your resume, and the Google Gemini AI will read it, extract your skills and experiences, and automatically build your portfolio layout for you.

## Features

- **AI Resume Parsing**: Powered by Google Gemini 2.5 Flash and PyMuPDF, automatically extract your `Skills` and `Work Experience` from a PDF resume.
- **Admin Dashboard**: Manage your complete site configuration including Hero sections, About Me texts, Educations, and Projects behind a secure login.
- **Dynamic Frontend**: Modern Jinja2 templates handle the clean, responsive layout out of the box.
- **Custom Ordering**: Re-order timeline experiences, educations, and projects accurately.
- **Render Ready**: Includes automatic deployment blueprints (`render.yaml`), strict dependency mapping (`requirements.txt` with Gunicorn), and `.python-version` configured for Python 3.11 for 1-click Render.com deployment.

## Tech Stack

- **Backend**: Python 3.11, Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **AI Processing**: Google GenAI SDK (`gemini-2.5-flash`), PyMuPDF
- **Frontend**: HTML5, CSS3, Jinja2 Templating
- **Production Server**: Gunicorn

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/portfolio_website.git
cd portfolio_website
```

### 2. Create a Virtual Environment and Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create a `.env` File
Create a `.env` file in the root of the project with the following keys:
```env
SECRET_KEY=your_secure_flask_secret_key
ADMIN_PASSWORD=your_dashboard_password
GEMINI_API_KEY=your_google_gemini_api_key
```
*(You can get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey))*

### 4. Run the Application
```bash
python app.py
```
The application will be running at `http://localhost:5000`. 
Head to `http://localhost:5000/login` to access the Admin Panel.

## Deployment (Render.com)
This app is strictly configured for instant deployment to Render.
1. Create a [Render](https://render.com) account.
2. Go to **Blueprints** -> **New Blueprint Instance**.
3. Connect your GitHub repository. The `render.yaml` file will configure the Python Environment, Gunicorn start commands, and necessary package management automatically.
4. Add your `.env` variables into Render's Environment Variables panel.

## AI Parser Usage
1. Log into your Admin Dashboard (`/admin`).
2. Scroll to the "AI Resume Parser" section.
3. Upload your `.pdf` resume.
4. Watch as your new skills and work experience seamlessly populate into the database and appear live on your site!
