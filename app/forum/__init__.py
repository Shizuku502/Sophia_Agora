# app/forum/__init__.py

from .route import forum_bp

def register_forum_blueprint(app):
    app.register_blueprint(forum_bp)