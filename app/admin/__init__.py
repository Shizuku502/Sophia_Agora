# app/admin/__init__.py

from .route import admin_bp

def register_admin_blueprint(app):
    app.register_blueprint(admin_bp)