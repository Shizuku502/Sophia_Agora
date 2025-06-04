# app/models/teacher_schedule.py

from app.extensions import db
from datetime import datetime

class Teacher_Schedule(db.Model):
    __tablename__ = 'teacher_schedules'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weekday = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship('User', backref=db.backref('personal_schedules', lazy='dynamic'))

    def __repr__(self):
        return f"<Teacher_Schedule {self.course_name} on {self.weekday} from {self.start_time} to {self.end_time}>"
