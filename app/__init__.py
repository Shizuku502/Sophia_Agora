from flask import Flask
from app.extensions import db, login_manager, migrate
from .auth import register_auth_blueprint
from .admin import register_admin_blueprint
from .forum import register_forum_blueprint
from .main import register_main_blueprint
from .user import register_user_blueprint
from .notification import register_notification_blueprint
from .report import register_report_blueprint
from .utils import filters


def create_app(config_class="app.config.DevelopmentConfig"):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .models import user, post, comment, reaction, forbidden_word, notification, report

    register_auth_blueprint(app)
    register_admin_blueprint(app)
    register_forum_blueprint(app)
    register_main_blueprint(app)
    register_user_blueprint(app)
    register_notification_blueprint(app)
    register_report_blueprint(app)
    
    
    # 註冊自訂濾鏡
    app.jinja_env.filters['format_datetime'] = filters.format_datetime
    app.jinja_env.filters['censor_text'] = filters.censor_text
    app.jinja_env.filters['utc_span'] = filters.utc_span

    return app