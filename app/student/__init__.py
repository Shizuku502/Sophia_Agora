# app/student/__init__.py

from .schedule import student_schedule_bp

def register_student_schedule_blueprint(app):
    app.register_blueprint(student_schedule_bp)