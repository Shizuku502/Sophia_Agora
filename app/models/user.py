# app/models/user.py

from flask import url_for
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
    email = db.Column(db.String(120), unique=True)
    extension = db.Column(db.String(20))
    last_login = db.Column(db.DateTime, default=None)
    registered_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    nickname = db.Column(db.String(100), default="未設定", nullable=False)
    teacher_id = db.Column(db.String(10), default=None)
    student_id = db.Column(db.String(10), default=None)
    avatar_filename = db.Column(db.String(100), default='default.jpg')
    points = db.Column(db.Integer, nullable=False, default=100, server_default="100")
    is_suspended = db.Column(db.Boolean, default=False)
    
    
    notifications = db.relationship('Notification', back_populates='user', lazy='dynamic')
    teacher_papers = db.relationship('Teacher_Paper', backref='teacher', lazy='dynamic')
    teacher_experiences = db.relationship('Teacher_Experience', backref='teacher', lazy='dynamic')
    teacher_expertises = db.relationship('Teacher_Expertise', backref='teacher', lazy='select')


    def __repr__(self):
        return f'<User {self.account_id}, Role: {self.role}>'

    def set_password(self, password):
        """加密並儲存密碼"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """檢查密碼是否正確"""
        return check_password_hash(self.password_hash, password)

    def deduct_points(self, amount):
        """扣除使用者分數，不能低於 0 分"""
        if self.points is None:
            self.points = 100
        self.points = max(0, self.points - amount)

    @property
    def is_admin(self):
        """判斷使用者是否為管理員"""
        return self.role == 'admin'

    @property
    def display_name(self):
        """回傳使用者暱稱，若無設定則回傳帳號"""
        return self.nickname if self.nickname.strip() else self.account_id

    @property
    def avatar_url(self):
        if self.avatar_filename:
            return url_for('static', filename=f'uploads/avatars/{self.avatar_filename}', _external=False)
        else:
            return url_for('static', filename='uploads/avatars/default.jpg', _external=False)

    def can_participate(self):
        """判斷使用者是否有權限進行貼文、留言、按讚等操作"""
        # 管理員永遠有權限
        if self.is_admin:
            return True
        # 非管理員需判斷是否被停權與分數
        return not self.is_suspended and self.points >= 80