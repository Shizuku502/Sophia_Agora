# app/forum/comment.py

from flask import Blueprint, request, redirect, render_template, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.comment import Comment
from app.models.post import Post
from app.models.notification import Notification
from app.utils.helpers import sanitize_content

comment_bp = Blueprint("comment", __name__, url_prefix="/comments")

@comment_bp.route("/create", methods=["POST"])
@login_required
def add_comment():
    post_id = request.form["post_id"]
    content = sanitize_content(request.form["content"])
    
    # 建立留言
    comment = Comment(post_id=post_id, user_id=current_user.id, content=content)
    db.session.add(comment)
    
    # 建立通知
    post = Post.query.get(post_id)
    if post and post.user_id != current_user.id:
        notification = Notification(
            user_id = post.user_id,
            type = "comment",
            content=f"{current_user.nickname} 回覆了你的貼文「{post.title}」",
            link=url_for("post.post_detail", post_id=post.id),
            is_read=False
        )
        db.session.add(notification)
        
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

# ✅ 編輯留言 - 接收表單資料並更新
@comment_bp.route("/<int:comment_id>/edit", methods=["GET"])
@login_required
def edit_comment_form(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)
    return render_template("comments/edit_comment.html", comment=comment)

@comment_bp.route("/<int:comment_id>/edit", methods=["POST"])
@login_required
def edit_comment_submit(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)

    content = sanitize_content(request.form.get("content"))
    if not content:
        flash("留言內容不能為空", "danger")
        return redirect(url_for("comment.edit_comment_form", comment_id=comment.id))

    comment.content = content
    db.session.commit()

    flash("留言已成功更新", "success")
    return redirect(url_for("post.post_detail", post_id=comment.post_id))

# 取得單一留言的API

@comment_bp.route("/<int:comment_id>/json")
@login_required
def get_comment_json(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    return {
        "id": comment.id,
        "content": comment.content
    }
