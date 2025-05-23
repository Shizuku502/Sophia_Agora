# app/__init__.py

from flask import Flask
import secrets

# Extensions
from .extensions import db, login_manager, migrate

# 藍圖註冊器
from .auth import register_auth_blueprint
from .admin import register_admin_blueprint
from .forum import register_forum_blueprint

def create_app():
    app = Flask(__name__, static_folder="static")
    app.secret_key = secrets.token_hex(16)

    # 設定資料庫連線
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://Kao:zxc12359@localhost/forum_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化擴充套件
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 匯入模型（確保 SQLAlchemy 能看到）
    from .models import user, post, comment, reaction, forbidden_word

    # 註冊所有 blueprint
    register_auth_blueprint(app)
    register_admin_blueprint(app)
    register_forum_blueprint(app)

    return app