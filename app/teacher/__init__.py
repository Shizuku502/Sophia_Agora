# app/teacher/__init__.py

from .route import teacher_bp

def register_teacher_blueprint(app):
    app.register_blueprint(teacher_bp)