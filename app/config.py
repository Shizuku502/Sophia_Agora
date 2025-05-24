import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Kao:zxc12359@localhost/forum_db"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///prod.db")
    SQLALCHEMY_ECHO = False  # 生產環境不建議顯示 SQL

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True