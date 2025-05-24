from .route import main_bp

def register_main_blueprint(app):
    app.register_blueprint(main_bp)