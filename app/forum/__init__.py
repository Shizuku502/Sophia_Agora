# forum/__init__.py

from .post import post_bp
from .comment import comment_bp
from .reaction import reaction_bp
from .route import forum_bp

def register_forum_blueprint(app):
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(reaction_bp)
    app.register_blueprint(forum_bp)