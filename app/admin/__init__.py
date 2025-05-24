# app/admin/__init__.py

from .route import admin_bp

def register_admin_blueprint(app):
    from .admin_user import admin_user_bp
    from .admin_post import admin_post_bp
    from .admin_comment import admin_comment_bp
    from .admin_forbidden_word import admin_forbidden_word_bp

   
    app.register_blueprint(admin_bp, url_prefix="/admin", name="admin_main")
    app.register_blueprint(admin_user_bp, name="admin_user")
    app.register_blueprint(admin_post_bp, name="admin_post")
    app.register_blueprint(admin_comment_bp, name="admin_comment")
    app.register_blueprint(admin_forbidden_word_bp, name="admin_forbidden_word")