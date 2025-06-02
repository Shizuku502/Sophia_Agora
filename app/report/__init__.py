from .route import report_bp

def register_report_blueprint(app):
    app.register_blueprint(report_bp)