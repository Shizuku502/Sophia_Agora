# app/teacher/__init__.py

from .route import teacher_bp

def register_teacher_blueprint(app):
    app.register_blueprint(teacher_bp)
    

from .schedule import teacher_schedule_bp

def register_teacher_schedule_blueprint(app):
    app.register_blueprint(teacher_schedule_bp)