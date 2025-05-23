# app/auth/__init__.py

from .route import auth_bp

def register_auth_blueprint(app):
    app.register_blueprint(auth_bp)