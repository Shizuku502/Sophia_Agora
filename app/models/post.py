# .models/post.py

from datetime import datetime
from app.extensions import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="posts")
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan", lazy=True)
    reactions = db.relationship("Reaction", backref="post", cascade="all, delete-orphan", lazy="dynamic")

    # 避免 circular import，使用字串指定模型名稱
    edit_history = db.relationship(
        "Post_Edit_History",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    @property
    def like_count(self):
        return self.reactions.filter_by(type="like").count()

    @property
    def dislike_count(self):
        return self.reactions.filter_by(type="dislike").count()