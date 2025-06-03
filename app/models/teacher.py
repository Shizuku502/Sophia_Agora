# app/models/teacher.py

from app.extensions import db

class Teacher_Paper(db.Model):
    __tablename__ = 'teacher_papers'
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(7), nullable=False)
    paper_type = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Teacher_Experience(db.Model):
    __tablename__ = 'teacher_experiences'
    id = db.Column(db.String(10), primary_key=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Teacher_Expertise(db.Model):
    __tablename__ = 'teacher_expertises'
    id = db.Column(db.String(10), primary_key=True)
    field = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
