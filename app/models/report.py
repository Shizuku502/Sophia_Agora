# models/report.py
from app.extensions import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # 三擇一：只能檢舉其中一種目標
    reported_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reported_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    reported_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)

    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending / approved / rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    reported_user = db.relationship('User', foreign_keys=[reported_user_id])
    reported_post = db.relationship('Post', foreign_keys=[reported_post_id])
    reported_comment = db.relationship('Comment', foreign_keys=[reported_comment_id])