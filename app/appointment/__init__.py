# app/appointment/__init__.py

from .route import appointment_bp

def register_appointment_blueprint(app):
    app.register_blueprint(appointment_bp)