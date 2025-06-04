# app/models/teacher_available_schedule.py

from app.extensions import db
from datetime import datetime

class Teacher_Available_Schedule(db.Model):
    __tablename__ = 'teacher_available_schedules'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weekday = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)  # 是否開放學生預約
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship('User', backref=db.backref('available_slots', lazy='dynamic'))
