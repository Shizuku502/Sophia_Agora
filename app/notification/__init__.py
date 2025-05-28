# app/notification/__init__.py

from .route import notification_bp

def register_notification_blueprint(app):
    app.register_blueprint(notification_bp)