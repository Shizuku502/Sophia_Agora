# app/models/student_schedule.py

from app.extensions import db
from datetime import datetime

class Student_Schedule(db.Model):
    __tablename__ = 'student_schedules'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weekday = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref=db.backref('personal_courses', lazy='dynamic'))
