from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import json
from dotenv import load_dotenv
from functools import wraps
from google import genai
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_for_dev_only')
db_url = os.environ.get('DATABASE_URL', 'sqlite:///portfolio.db')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# Configure Gemini
api_key = os.environ.get('GEMINI_API_KEY')
client = None
if api_key and api_key != 'YOUR_GEMINI_API_KEY_HERE':
    client = genai.Client(api_key=api_key)

# Models
class SiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_title = db.Column(db.String(255), nullable=False)
    hero_subtitle = db.Column(db.String(255), nullable=False)
    hero_description = db.Column(db.Text, nullable=False)
    about_text = db.Column(db.Text, nullable=False)
    about_image_path = db.Column(db.String(255), nullable=True)
    resume_file_path = db.Column(db.String(255), nullable=True)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon_class = db.Column(db.String(50), nullable=False)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    period = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    github_link = db.Column(db.String(255), nullable=True)
    external_link = db.Column(db.String(255), nullable=True)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    period = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

# Auth Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Public Routes
@app.route('/')
def home():
    site_content = SiteContent.query.first()
    skills = Skill.query.all()
    experiences = Experience.query.order_by(Experience.display_order.asc()).all()
    projects = Project.query.order_by(Project.display_order.asc()).all()
    educations = Education.query.order_by(Education.display_order.asc()).all()
    
    for project in projects:
        project.tag_list = [tag.strip() for tag in project.tags.split(',') if tag.strip()]

    return render_template('index.html', 
                           site_content=site_content,
                           skills=skills, 
                           experiences=experiences, 
                           projects=projects, 
                           educations=educations)

# Admin Auth Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.environ.get('ADMIN_PASSWORD'):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

# Admin Dashboard
@app.route('/admin')
@login_required
def admin():
    site_content = SiteContent.query.first()
    skills = Skill.query.all()
    experiences = Experience.query.order_by(Experience.display_order.asc()).all()
    projects = Project.query.order_by(Project.display_order.asc()).all()
    educations = Education.query.order_by(Education.display_order.asc()).all()
    return render_template('admin.html', 
                           site_content=site_content, 
                           skills=skills, 
                           experiences=experiences,
                           projects=projects,
                           educations=educations)

# --- Site Content Route ---
@app.route('/admin/sitecontent/update', methods=['POST'])
@login_required
def admin_update_site_content():
    content = SiteContent.query.first()
    if not content:
        content = SiteContent()
        db.session.add(content)
        
    content.hero_title = request.form.get('hero_title') or content.hero_title
    content.hero_subtitle = request.form.get('hero_subtitle') or content.hero_subtitle
    content.hero_description = request.form.get('hero_description') or content.hero_description
    content.about_text = request.form.get('about_text') or content.about_text
    
    if 'about_image' in request.files:
        img = request.files['about_image']
        if img.filename:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.root_path, 'static/assets', filename))
            content.about_image_path = filename
            
    if 'resume_file' in request.files:
        res = request.files['resume_file']
        if res.filename:
            filename = secure_filename(res.filename)
            res.save(os.path.join(app.root_path, 'static/assets', filename))
            content.resume_file_path = filename

    db.session.commit()
    flash('Site content updated successfully!', 'success')
    return redirect(url_for('admin'))

# --- Skills CRUD ---
@app.route('/admin/skill/add', methods=['POST'])
@login_required
def admin_add_skill():
    name = request.form.get('name')
    icon_class = request.form.get('icon_class')
    if name and icon_class:
        db.session.add(Skill(name=name, icon_class=icon_class))
        db.session.commit()
        flash('Skill added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/skill/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted.', 'success')
    return redirect(url_for('admin'))

# --- Experience CRUD ---
@app.route('/admin/experience/add', methods=['POST'])
@login_required
def admin_add_experience():
    period = request.form.get('period')
    title = request.form.get('title')
    company = request.form.get('company')
    description = request.form.get('description')
    
    image_path = None
    if 'image' in request.files:
        img = request.files['image']
        if img.filename:
            image_path = secure_filename(img.filename)
            img.save(os.path.join(app.root_path, 'static/assets', image_path))
            
    if period and title and company:
        db.session.add(Experience(period=period, title=title, company=company, description=description, image_path=image_path))
        db.session.commit()
        flash('Experience added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/experience/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_experience(id):
    exp = Experience.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    flash('Experience deleted.', 'success')
    return redirect(url_for('admin'))

# --- Project CRUD ---
@app.route('/admin/project/add', methods=['POST'])
@login_required
def admin_add_project():
    title = request.form.get('title')
    description = request.form.get('description')
    tags = request.form.get('tags')
    github_link = request.form.get('github_link')
    external_link = request.form.get('external_link')
    
    image_path = None
    if 'image' in request.files:
        img = request.files['image']
        if img.filename:
            image_path = secure_filename(img.filename)
            img.save(os.path.join(app.root_path, 'static/assets', image_path))
            
    if title and description:
        db.session.add(Project(title=title, description=description, tags=tags, image_path=image_path, github_link=github_link, external_link=external_link))
        db.session.commit()
        flash('Project added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/project/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_project(id):
    proj = Project.query.get_or_404(id)
    db.session.delete(proj)
    db.session.commit()
    flash('Project deleted.', 'success')
    return redirect(url_for('admin'))

# --- Education CRUD ---
@app.route('/admin/education/add', methods=['POST'])
@login_required
def admin_add_education():
    period = request.form.get('period')
    degree = request.form.get('degree')
    institution = request.form.get('institution')
    description = request.form.get('description')
    
    if period and degree and institution:
        db.session.add(Education(period=period, degree=degree, institution=institution, description=description))
        db.session.commit()
        flash('Education added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/education/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_education(id):
    edu = Education.query.get_or_404(id)
    db.session.delete(edu)
    db.session.commit()
    flash('Education deleted.', 'success')
    return redirect(url_for('admin'))

# --- Ordering Route ---
@app.route('/admin/order/update', methods=['POST'])
@login_required
def admin_update_order():
    # Expects form data like: exp_1=10, proj_2=20, edu_1=5
    for key, value in request.form.items():
        if not value.isdigit():
            continue
        order_val = int(value)
        if key.startswith('exp_'):
            exp_id = int(key.split('_')[1])
            exp = Experience.query.get(exp_id)
            if exp: exp.display_order = order_val
        elif key.startswith('proj_'):
            proj_id = int(key.split('_')[1])
            proj = Project.query.get(proj_id)
            if proj: proj.display_order = order_val
        elif key.startswith('edu_'):
            edu_id = int(key.split('_')[1])
            edu = Education.query.get(edu_id)
            if edu: edu.display_order = order_val
    
    db.session.commit()
    flash('Display orders updated!', 'success')
    return redirect(url_for('admin'))

# AI Resume Parser Route
@app.route('/admin/parse_resume', methods=['POST'])
@login_required
def admin_parse_resume():
    if not os.environ.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY') == 'YOUR_GEMINI_API_KEY_HERE':
        flash('Gemini API Key is not configured. Please set GEMINI_API_KEY in .env', 'error')
        return redirect(url_for('admin'))

    if 'resume' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('admin'))
        
    file = request.files['resume']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin'))

    try:
        text = ""
        if file.filename.endswith('.pdf'):
            pdf_bytes = file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text()
        else:
            text = file.read().decode('utf-8')
            
        if not client:
            flash('Gemini API Key is not configured properly.', 'error')
            return redirect(url_for('admin'))

        prompt = """
        Parse the following resume text and extract the skills and experiences.
        Return STRICTLY a JSON object with this exact shape:
        {
          "skills": [
            { "name": "string", "icon_class": "string (closest lucide icon name like code-2, database, server, etc.)" }
          ],
          "experience": [
            { "period": "string (e.g. Jan 2020 - Present)", "title": "string", "company": "string", "description": "string", "image_path": "" }
          ]
        }
        Do not wrap the output in markdown code blocks. Output raw JSON only.
        
        Resume Text:
        """ + text
        
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        result_text = response.text.strip()
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]
            
        data = json.loads(result_text.strip())
        
        skills_added = 0
        for s in data.get('skills', []):
            if not Skill.query.filter_by(name=s['name']).first():
                db.session.add(Skill(name=s['name'], icon_class=s['icon_class']))
                skills_added += 1
                
        exps_added = 0
        for e in data.get('experience', []):
            if not Experience.query.filter_by(title=e['title'], company=e['company']).first():
                # For newly parsed experiences, default to order 0
                db.session.add(Experience(period=e['period'], title=e['title'], company=e['company'], description=e['description'], image_path=e.get('image_path', '')))
                exps_added += 1
                
        db.session.commit()
        flash(f'Successfully parsed resume! Added {skills_added} skills and {exps_added} experiences.', 'success')
        
    except Exception as e:
        flash(f'Error parsing resume: {str(e)}', 'error')
        
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
