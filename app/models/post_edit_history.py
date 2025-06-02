# app/models/post_edit_history.py

from datetime import datetime
from app.extensions import db

class Post_Edit_History(db.Model):
    __tablename__ = "post_edit_history"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    editor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    original_title = db.Column(db.String(255))
    original_content = db.Column(db.Text, nullable=False)
    edited_at = db.Column(db.DateTime, default=datetime.utcnow)

    post = db.relationship("Post", back_populates="edit_history")
    editor = db.relationship("User", backref="edited_posts")
