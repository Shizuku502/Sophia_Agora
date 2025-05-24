from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
migrate = Migrate()

from app.models.user import User  # ✅ 確保這行存在

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))