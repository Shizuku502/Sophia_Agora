from datetime import datetime
from app.extensions import db
from app.models.user import User  # ✅ 確保有這一行

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', backref='posts')  # ✅ 加這一行

    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy=True)
    reactions = db.relationship('Reaction', backref='post', cascade="all, delete-orphan" ,lazy=True)
