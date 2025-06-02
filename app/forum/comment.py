#.forum/comment.py

from flask import Blueprint, request, redirect, render_template, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.comment import Comment
from app.models.post import Post
from app.models.comment_edit_history import Comment_Edit_History
from app.models.notification import Notification
from app.utils.helpers import sanitize_content

comment_bp = Blueprint("comment", __name__, url_prefix="/comments")

@comment_bp.route("/create", methods=["POST"])
@login_required
def add_comment():
    if not current_user.can_participate():
        flash("您的分數過低（須達 80 分），無法留言。", "danger")
        return redirect(url_for("post.post_detail", post_id=request.form.get("post_id")))

    post_id = request.form.get("post_id")
    content = sanitize_content(request.form.get("content"))

    if not content:
        flash("留言內容不得為空", "warning")
        return redirect(url_for("post.post_detail", post_id=post_id))

    comment = Comment(post_id=post_id, user_id=current_user.id, content=content)
    db.session.add(comment)

    post = Post.query.get(post_id)
    if post and post.user_id != current_user.id:
        notification = Notification(
            user_id=post.user_id,
            type="comment",
            content=f"{current_user.nickname} 回覆了你的貼文「{post.title}」",
            link=url_for("post.post_detail", post_id=post.id),
            is_read=False
        )
        db.session.add(notification)

    db.session.commit()
    flash("留言成功", "success")
    return redirect(url_for("post.post_detail", post_id=post_id))

@comment_bp.route("/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user.id != comment.user_id and not current_user.is_admin:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash("留言已刪除", "info")
    return redirect(url_for("post.post_detail", post_id=comment.post_id))

@comment_bp.route("/<int:comment_id>/edit", methods=["GET"])
@login_required
def edit_comment_form(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)
    return render_template("comments/edit_comment.html", comment=comment)

@comment_bp.route("/<int:comment_id>/edit", methods=["POST"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)

    new_content = sanitize_content(request.form.get("content"))
    if comment.content != new_content:
        history = Comment_Edit_History(
            comment_id=comment.id,
            editor_id=current_user.id,
            original_content=comment.content,
            edited_at=db.func.now()
        )
        db.session.add(history)
        comment.content = new_content
        db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return "", 204

    return redirect(url_for("post.post_detail", post_id=comment.post_id))

@comment_bp.route("/<int:comment_id>/history")
@login_required
def comment_history(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user.id != comment.user_id and not current_user.is_admin:
        abort(403)

    history = Comment_Edit_History.query.filter_by(comment_id=comment_id)\
        .order_by(Comment_Edit_History.edited_at.desc()).all()

    return render_template("forum/comment_history_modal.html", history=history)

@comment_bp.route("/<int:comment_id>/json")
@login_required
def get_comment_json(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)

    return jsonify({
        "id": comment.id,
        "content": comment.content
    })