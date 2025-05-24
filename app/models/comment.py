from datetime import datetime
from app.extensions import db

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)

    replies = db.relationship(
        'Comment',
        backref=db.backref('parent', remote_side=[id]),
        cascade="all, delete-orphan",
        lazy='dynamic'
    )
    user = db.relationship('User', backref='comments')
    reactions = db.relationship('Reaction', backref='comment', lazy=True)