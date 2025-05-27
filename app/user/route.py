# app/user/route.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.extensions import db
from app.user.form import EditProfileForm
from sqlalchemy import func
from PIL import Image
from app.utils.image import compress_and_save_image
import uuid 
import os

user_bp = Blueprint(
    "user",
    __name__, 
    url_prefix="/user", 
    template_folder='templates'
)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    comments = Comment.query.filter_by(user_id=user_id).order_by(Comment.created_at.desc()).all()
    total_likes = sum(post.like_count for post in posts)

    return render_template(
        'user/profile.html',
        user=user,
        posts=posts,
        comments=comments,
        total_likes=total_likes
    )


@user_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.nickname = form.nickname.data or current_user.nickname

        # ✅ 如果勾選「移除頭像」
        if form.remove_avatar.data:
            if current_user.avatar_filename and current_user.avatar_filename != 'default.jpg':
                old_path = os.path.join(
                    current_app.root_path, 'static', 'uploads', 'avatars', current_user.avatar_filename
                )
                if os.path.exists(old_path):
                    os.remove(old_path)
            current_user.avatar_filename = 'default.jpg'

        # ✅ 如果有上傳新頭像（要排除與刪除同時發生的情況）
        elif form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            ext = filename.rsplit('.', 1)[-1].lower()

            if not allowed_file(filename):
                flash('請上傳 jpg, jpeg 或 png 格式的圖片。', 'danger')
                return redirect(request.url)

            avatar_filename = f"user_{current_user.id}_{uuid.uuid4().hex[:8]}.{ext}"
            upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
            os.makedirs(upload_path, exist_ok=True)
            avatar_path = os.path.join(upload_path, avatar_filename)

            try:
                compress_and_save_image(form.avatar.data, avatar_path)
                current_user.avatar_filename = avatar_filename
            except Exception as e:
                db.session.rollback()
                flash(f'頭像處理失敗：{str(e)}', 'danger')
                return redirect(request.url)

        try:
            db.session.commit()
            flash('個人資料已更新', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'更新失敗：{str(e)}', 'danger')
            return redirect(request.url)

        return redirect(url_for('user.profile', user_id=current_user.id))

    if request.method == 'GET':
        form.nickname.data = current_user.nickname

    return render_template('user/edit_profile.html', form=form)