from datetime import datetime
from app.extensions import db

class Reaction(db.Model):
    __tablename__ = "reactions"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('like', 'dislike', name='reaction_type'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)

    __table_args__ = (
        db.CheckConstraint(
            "(post_id IS NOT NULL AND comment_id IS NULL) OR (post_id IS NULL AND comment_id IS NOT NULL)",
            name="check_post_or_comment_only"
        ),
    )