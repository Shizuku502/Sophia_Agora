# app/models/appointment.py

from app.extensions import db
from datetime import datetime
from sqlalchemy import Enum

appointment_status = Enum('pending', 'accepted', 'rejected', 'cancelled', name='appointment_status')

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(appointment_status, default='pending')
    rejection_reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=True)  
    note = db.Column(db.Text, nullable=True) 
    
    student = db.relationship('User', foreign_keys=[student_id], backref=db.backref('appointments_made', lazy='dynamic'))
    teacher = db.relationship('User', foreign_keys=[teacher_id], backref=db.backref('appointments_received', lazy='dynamic'))