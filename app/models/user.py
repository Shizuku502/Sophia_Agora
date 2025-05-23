from flask_login import UserMixin
from datetime import datetime
from extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', 'admin', name='user_roles'), nullable=False)
    status = db.Column(db.Enum('online', 'busy', 'offline', name='user_status'), default='offline')
    last_login = db.Column(db.DateTime, default=None)
    registered_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    nickname = db.Column(db.String(100), default="未設定", nullable=False)
    teacher_id = db.Column(db.String(10), default=None)
    student_id = db.Column(db.String(10), default=None)

    def __repr__(self):
        return f'<User {self.account_id}, Role: {self.role}>'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def display_name(self):
        return self.nickname if self.nickname else self.account_id