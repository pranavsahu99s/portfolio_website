from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_for_dev_only')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon_class = db.Column(db.String(50), nullable=False)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(255), nullable=False) # Comma-separated
    image_path = db.Column(db.String(255), nullable=True)
    github_link = db.Column(db.String(255), nullable=True)
    external_link = db.Column(db.String(255), nullable=True)

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    skills = Skill.query.all()
    experiences = Experience.query.all()
    projects = Project.query.all()
    educations = Education.query.all()
    
    # Pre-process project tags for easy rendering
    for project in projects:
        project.tag_list = [tag.strip() for tag in project.tags.split(',') if tag.strip()]

    return render_template('index.html', 
                           skills=skills, 
                           experiences=experiences, 
                           projects=projects, 
                           educations=educations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
