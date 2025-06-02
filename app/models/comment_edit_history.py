# .models/comment_edit_history.py

from datetime import datetime
from app.extensions import db

class Comment_Edit_History(db.Model):
    __tablename__ = "comment_edit_history"

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)
    editor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    original_content = db.Column(db.Text, nullable=False)
    edited_at = db.Column(db.DateTime, default=datetime.utcnow)

    comment = db.relationship("Comment", back_populates="edit_history")
    editor = db.relationship("User", backref="edited_comments")
