from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from functools import wraps

from app.extensions import db
from app.models import User, ForbiddenWord, Post, Comment

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# --- 裝飾器：限制只有管理員能存取 ---
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for("main.homepage"))
        return func(*args, **kwargs)
    return decorated_view


# --- 使用者列表與搜尋功能 ---
@admin_bp.route("/users")
@login_required
@admin_required
def list_users():
    keyword = request.args.get("keyword", "").strip()
    role = request.args.get("role", "").strip()

    query = User.query
    if keyword:
        query = query.filter(User.account_id.contains(keyword))
    if role:
        query = query.filter(User.role == role)

    users = query.all()
    return render_template("admin/users.html", users=users, keyword=keyword, role=role)


# --- 新增使用者 ---
@admin_bp.route("/add_user", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():
    if request.method == "POST":
        account_id = request.form["account_id"].strip()
        password = request.form["password"]
        role = request.form["role"]
        nickname = request.form.get("nickname", "")

        if not role:
            first_char = account_id[0].upper()
            if first_char == "T":
                role = "teacher"
            elif first_char == "D":
                role = "student"
            elif first_char == "A":
                role = "admin"

        if User.query.filter_by(account_id=account_id).first():
            flash("帳號已存在", "danger")
            return redirect(url_for("admin.add_user"))

        new_user = User(
            account_id=account_id,
            password=generate_password_hash(password),
            role=role,
            nickname=nickname,
            status="offline"
        )

        if role == "student":
            new_user.student_id = account_id
        elif role == "teacher":
            new_user.teacher_id = account_id

        db.session.add(new_user)
        db.session.commit()
        flash("使用者新增成功", "success")
        return redirect(url_for("admin.list_users"))

    return render_template("admin/add_user.html")


# --- 刪除使用者 ---
@admin_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("使用者已刪除", "info")
    return redirect(url_for("admin.list_users"))


# --- 髒話管理：列出髒話 ---
@admin_bp.route("/forbidden_words")
@login_required
@admin_required
def list_forbidden_words():
    forbidden_words = ForbiddenWord.query.all()
    return render_template("admin/forbidden_words.html", forbidden_words=forbidden_words)


# --- 新增髒話 ---
@admin_bp.route("/add_forbidden_word", methods=["GET", "POST"])
@login_required
@admin_required
def add_forbidden_word():
    if request.method == "POST":
        word = request.form["word"].strip()
        if ForbiddenWord.query.filter_by(word=word).first():
            flash("該髒話已經存在！", "danger")
        else:
            new_word = ForbiddenWord(word=word)
            db.session.add(new_word)
            db.session.commit()
            flash("髒話已成功新增！", "success")
        return redirect(url_for("admin.list_forbidden_words"))
    return render_template("admin/add_forbidden_word.html")


# --- 刪除髒話 ---
@admin_bp.route("/delete_forbidden_word/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_forbidden_word(id):
    forbidden_word = ForbiddenWord.query.get(id)
    if forbidden_word:
        db.session.delete(forbidden_word)
        db.session.commit()
        flash("髒話已成功刪除！", "info")
    return redirect(url_for("admin.list_forbidden_words"))


# --- 刪除貼文 ---
@admin_bp.route("/delete_post/<int:post_id>", methods=["POST"])
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("此貼文已刪除", "info")
    else:
        flash("找不到此貼文", "danger")
    return redirect(url_for("forum.index"))


# --- 刪除留言 ---
@admin_bp.route("/delete_comment/<int:comment_id>", methods=["POST"])
@login_required
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        flash("此留言已刪除", "info")
    else:
        flash("找不到此留言", "danger")
    return redirect(url_for("forum.post_detail"))