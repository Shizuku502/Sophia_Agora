# app/forum/post.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.post import Post
from app.models.comment import Comment
from app.models.post_edit_history import Post_Edit_History
from app.utils.helpers import sanitize_content

post_bp = Blueprint("post", __name__, url_prefix="/posts")

@post_bp.route("/")
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("forum/index.html", posts=posts)

@post_bp.route("/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("forum/post_detail.html", post=post)

@post_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if not current_user.can_participate():
        flash("您的分數過低（須達 80 分），無法發表文章。", "danger")
        return redirect(url_for("post.list_posts"))

    if request.method == "POST":
        title = request.form["title"]
        content = sanitize_content(request.form["content"])
        post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("已成功發佈文章")
        return redirect(url_for("post.list_posts"))

    return render_template("forum/add_post.html")

@post_bp.route("/edit/<int:post_id>", methods=["GET"])
@login_required
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    return render_template("forum/edit_post.html", post=post)

@post_bp.route("/edit/<int:post_id>", methods=["POST"])
@login_required
def edit_post_submit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)

    title = request.form.get("title")
    content = sanitize_content(request.form.get("content"))

    if not title or not content:
        flash("標題和內容都不能空白。", "danger")
        return redirect(url_for("post.edit_post_form", post_id=post.id))

    # 紀錄編輯歷史（僅當內容有變動）
    if post.title != title or post.content != content:
        history = Post_Edit_History(
            post_id=post.id,
            editor_id=current_user.id,
            original_title=post.title,
            original_content=post.content
        )
        db.session.add(history)

        post.title = title
        post.content = content
        db.session.commit()

    flash("文章已成功更新！", "success")
    return redirect(url_for("post.post_detail", post_id=post.id))

@post_bp.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    # 刪除關聯的留言與編輯歷史紀錄
    Comment.query.filter_by(post_id=post.id).delete()
    Post_Edit_History.query.filter_by(post_id=post.id).delete()

    db.session.delete(post)
    db.session.commit()
    flash("文章已成功刪除。", "success")
    return redirect(url_for("post.list_posts"))



@post_bp.route("/<int:post_id>/history")
@login_required
def post_history(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.user_id and not current_user.is_admin:
        abort(403)
    history = Post_Edit_History.query.filter_by(post_id=post_id).order_by(Post_Edit_History.edited_at.desc()).all()
    return render_template("forum/post_history_modal.html", history=history)