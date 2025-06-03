# app/teacher/route.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models.teacher import Teacher_Paper, Teacher_Experience, Teacher_Expertise
from app.utils.decorators import teacher_required
import uuid
import os
import re
from werkzeug.utils import secure_filename


teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher",
    template_folder="templates"
)

# 教師個人學經歷頁面
@teacher_bp.route("/profile", methods=["GET", "POST"])
@login_required
@teacher_required
def profile():
    if request.method == "POST":
        nickname = request.form.get("nickname", "").strip()
        email = request.form.get("email", "").strip()
        extension = request.form.get("extension", "").strip()
        avatar_file = request.files.get("avatar")

        if nickname:
            current_user.nickname = nickname
        if email:
            current_user.email = email
        if extension:
            current_user.extension = extension

        if avatar_file and avatar_file.filename != "":
            filename = secure_filename(avatar_file.filename)
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            if ext not in allowed_extensions:
                flash("請上傳 png, jpg, jpeg, gif 格式的圖片", "error")
                return redirect(url_for("teacher.profile"))
            
            new_filename = f"avatar_{current_user.id}.{ext}"
            upload_path = os.path.join(current_app.root_path, "static", "uploads", "avatars")
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, new_filename)
            avatar_file.save(file_path)
            current_user.avatar_filename = new_filename

        db.session.commit()
        flash("個人資料更新成功", "success")
        return redirect(url_for("teacher.profile"))

    teacher_id = current_user.id
    papers = Teacher_Paper.query.filter_by(teacher_id=teacher_id).all()
    experiences = Teacher_Experience.query.filter_by(teacher_id=teacher_id).all()
    expertises = Teacher_Expertise.query.filter_by(teacher_id=teacher_id).all()

    from app.models.post import Post
    from app.models.comment import Comment

    posts = Post.query.filter_by(user_id=teacher_id).all()
    comments = Comment.query.filter_by(user_id=teacher_id).all()
    total_likes = sum(post.like_count for post in posts)

    return render_template(
        "teacher/profile.html",
        user=current_user,
        papers=papers,
        experiences=experiences,
        expertises=expertises,
        posts=posts,
        comments=comments,
        total_likes=total_likes
    )


# 新增論文    
@teacher_bp.route("/papers/add", methods=["GET", "POST"])
@login_required
@teacher_required
def add_paper():
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        paper_type = request.form.get("paper_type")

        # 基本檢查
        if not title or not year or not paper_type:
            flash("請填寫所有欄位", "error")
            return redirect(url_for("teacher.add_paper"))

        new_paper = Teacher_Paper(
            id=str(uuid.uuid4())[:10],  # 簡化 UUID
            title=title,
            year=year,
            paper_type=paper_type,
            teacher_id=current_user.id
        )
        db.session.add(new_paper)
        db.session.commit()
        flash("論文新增成功")
        return redirect(url_for("teacher.profile"))

    return render_template("teacher/add_paper.html")

# 編輯論文
@teacher_bp.route("/papers/edit/<paper_id>", methods=["GET", "POST"])
@login_required
@teacher_required
def edit_paper(paper_id):
    paper = Teacher_Paper.query.filter_by(id=paper_id, teacher_id=current_user.id).first_or_404()

    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        paper_type = request.form.get("paper_type")

        # 基本檢查
        if not title or not year or not paper_type:
            flash("請填寫所有欄位", "error")
            return redirect(url_for("teacher.edit_paper", paper_id=paper_id))

        # 更新資料
        paper.title = title
        paper.year = year
        paper.paper_type = paper_type

        db.session.commit()
        flash("論文更新成功")
        return redirect(url_for("teacher.profile"))

    # GET 請求時，帶入論文資料到表單
    return render_template("teacher/edit_paper.html", paper=paper)

# 刪除論文
@teacher_bp.route("/papers/delete/<paper_id>", methods=["POST"])
@login_required
@teacher_required
def delete_paper(paper_id):
    paper = Teacher_Paper.query.get(paper_id)
    if paper is None:
        return jsonify(success=False, message="找不到貼文"), 404

    db.session.delete(paper)
    db.session.commit()
    return jsonify(success=True)

# 新增經歷
@teacher_bp.route("/experiences/add", methods=["GET", "POST"])
@login_required
@teacher_required
def add_experience():
    if request.method == "POST":
        description = request.form["description"].strip()
        category = request.form["category"].strip()

        if not description or not category:
            flash("所有欄位皆為必填", "error")
            return redirect(url_for("teacher_experience.add_experience"))

        new_experience = Teacher_Experience(
            id=f"EX{Teacher_Experience.query.count()+1:04}",
            description=description,
            category=category,
            teacher_id=current_user.id
        )

        db.session.add(new_experience)
        db.session.commit()
        flash("新增經歷成功", "success")
        return redirect(url_for("teacher.profile", user_id=current_user.id))

    return render_template("teacher/add_experience.html")

# 編輯經歷
@teacher_bp.route("/experiences/edit/<string:exp_id>", methods=["POST"])
@login_required
@teacher_required
def edit_experience(exp_id):
    data = request.get_json()
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()

    if not category or not description:
        return jsonify({"success": False, "error": "所有欄位皆為必填"}), 400

    experience = Teacher_Experience.query.filter_by(id=exp_id, teacher_id=current_user.id).first()
    if not experience:
        return jsonify({"success": False, "error": "找不到該經歷"}), 404

    experience.category = category
    experience.description = description

    try:
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": "資料庫更新失敗"}), 500
    
# 刪除經歷
@teacher_bp.route("/experiences/delete/<string:exp_id>", methods=["POST"])
@login_required
@teacher_required
def delete_experience(exp_id):
    experience = Teacher_Experience.query.filter_by(id=exp_id, teacher_id=current_user.id).first()
    if not experience:
        return jsonify({"success": False, "message": "找不到該經歷"}), 404

    try:
        db.session.delete(experience)
        db.session.commit()
        return jsonify({"success": True, "message": "經歷刪除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "刪除經歷失敗"}), 500

# 新增專長
@teacher_bp.route("/expertises/add", methods=["GET", "POST"])
@login_required
@teacher_required
def add_expertise():
    if request.method == "POST":
        field = request.form["field"].strip()

        if not field:
            flash("研究專長為必填欄位", "error")
            return redirect(url_for("teacher_expertise.add_expertise"))

        new_expertise = Teacher_Expertise(
            id=f"EP{Teacher_Expertise.query.count()+1:04}",
            field=field,
            teacher_id=current_user.id
        )

        db.session.add(new_expertise)
        db.session.commit()
        flash("研究專長新增成功", "success")
        return redirect(url_for("teacher.profile", user_id=current_user.id))

    return render_template("teacher/add_expertise.html")

# 編輯專長
@teacher_bp.route("/expertises/edit/<expertise_id>", methods=["POST"])
@login_required
@teacher_required
def ajax_edit_expertise(expertise_id):
    expertise = Teacher_Expertise.query.filter_by(id=expertise_id, teacher_id=current_user.id).first()
    if not expertise:
        return jsonify({"success": False, "message": "找不到專長"}), 404

    if request.is_json:
        data = request.get_json()
        new_field = data.get("field", "").strip()

        if not new_field:
            return jsonify({"success": False, "message": "專長不能為空"}), 400

        expertise.field = new_field
        db.session.commit()
        return jsonify({"success": True})

    return jsonify({"success": False, "message": "請使用正確的請求格式"}), 400

# 刪除專長
@teacher_bp.route("/expertises/delete/<expertise_id>", methods=["POST"])
@login_required
@teacher_required
def delete_expertise(expertise_id):
    expertise = Teacher_Expertise.query.filter_by(id=expertise_id, teacher_id=current_user.id).first()
    if not expertise:
        return jsonify({"success": False, "message": "找不到該專長"}), 404

    try:
        db.session.delete(expertise)
        db.session.commit()
        return jsonify({"success": True, "message": "專長刪除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "刪除專長失敗"}), 500

# 系所成員

from app.models.user import User

@teacher_bp.route('/teacher_list')
def teacher_list():
    teachers = User.query.filter_by(role='teacher').all()
    return render_template('teacher/teacher_list.html', teachers=teachers)

@teacher_bp.route('/public_profile/<account_id>')
def public_profile(account_id):
    teacher = User.query.filter_by(account_id=account_id, role='teacher').first_or_404()
    return render_template('teacher/public_profile.html', teacher=teacher)