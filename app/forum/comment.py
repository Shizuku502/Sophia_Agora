# app/forum/comment.py

from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.comment import Comment
from app.utils.helpers import sanitize_content

comment_bp = Blueprint("comment", __name__, url_prefix="/comments")

@comment_bp.route("/create", methods=["POST"])
@login_required
def add_comment():
    post_id = request.form["post_id"]
    content = sanitize_content(request.form["content"])
    comment = Comment(post_id=post_id, user_id=current_user.id, content=content)
    db.session.add(comment)
    db.session.commit()
    flash("留言成功")
    return redirect(url_for("post.post_detail", post_id=post_id))

@comment_bp.route("/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user.id == comment.user_id or current_user.is_admin:
        db.session.delete(comment)
        db.session.commit()
        flash("留言已刪除")
    return redirect(url_for("post.post_detail", post_id=comment.post_id))