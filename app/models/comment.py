# .models/comment.py

from datetime import datetime
from app.extensions import db

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)

    user = db.relationship("User", backref="comments")
    author = db.relationship("User", backref="comment", foreign_keys=[user_id])

    replies = db.relationship(
        "Comment",
        backref=db.backref("parent", remote_side=[id]),
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    reactions = db.relationship(
        "Reaction",
        backref="comment",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    edit_history = db.relationship(
        "Comment_Edit_History",
        back_populates="comment",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    # ✅ 自動刪除檢舉紀錄
    reports = db.relationship(
        "Report",
        backref="reported_comment_obj",
        cascade="all, delete-orphan",
        foreign_keys="[Report.reported_comment_id]",
        lazy="dynamic"
    )

    @property
    def like_count(self):
        return self.reactions.filter_by(type="like").count()

    @property
    def dislike_count(self):
        return self.reactions.filter_by(type="dislike").count()
