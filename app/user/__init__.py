# app/user/__init__.py

from .route import user_bp

def register_user_blueprint(app):
    app.register_blueprint(user_bp)

