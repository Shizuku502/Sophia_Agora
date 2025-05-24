# app/models/user.py

from flask_login import UserMixin
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(20), unique=True, nullable=False)  # 登入用帳號
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', 'admin', name='user_roles'), nullable=False)
    status = db.Column(db.Enum('online', 'busy', 'offline', name='user_status'), default='offline')
    last_login = db.Column(db.DateTime, default=None)
    registered_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    nickname = db.Column(db.String(100), default="未設定", nullable=False)
    teacher_id = db.Column(db.String(10), default=None)
    student_id = db.Column(db.String(10), default=None)

    def __repr__(self):
        return f'<User {self.account_id}, Role: {self.role}>'

    def set_password(self, password):
        """加密並儲存密碼"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """檢查密碼是否正確"""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        """判斷使用者是否為管理員"""
        return self.role == 'admin'

    @property
    def display_name(self):
        """回傳使用者暱稱，若無設定則回傳帳號"""
        return self.nickname if self.nickname else self.account_id
