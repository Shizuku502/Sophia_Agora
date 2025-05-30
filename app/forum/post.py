# app/forum/post.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.post import Post
from app.models.comment import Comment
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
    if request.method == "POST":
        title = request.form["title"]
        content = sanitize_content(request.form["content"])
        post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("已成功發佈文章")
        return redirect(url_for("post.list_posts"))
    return render_template("forum/add_post.html")

# ✅ 編輯文章 - 顯示表單
@post_bp.route("/edit/<int:post_id>", methods=["GET"])
@login_required
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    return render_template("forum/edit_post.html", post=post)

# ✅ 編輯文章 - 接收表單資料並更新
@post_bp.route("/edit/<int:post_id>", methods=["POST"])
@login_required
def edit_post_submit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)

    title = request.form.get("title")
    content = request.form.get("content")

    if not title or not content:
        flash("標題和內容都不能空白。", "danger")
        return redirect(url_for("post.edit_post_form", post_id=post.id))

    post.title = title
    post.content = content
    db.session.commit()

    flash("文章已成功更新！", "success")
    return redirect(url_for("post.post_detail", post_id=post.id)) 
