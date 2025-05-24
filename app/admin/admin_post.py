from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.extensions import db
from app.models.post import Post
from app.utils.decorators import admin_required

admin_post_bp = Blueprint('admin_post', __name__, url_prefix='/admin/posts')

@admin_post_bp.route('/')
@admin_required
def post_list():
    posts = Post.query.all()
    return render_template('admin/manage_post.html', posts=posts)

@admin_post_bp.route('/post/<int:post_id>')
@admin_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('admin/post_detail.html', post=post)

@admin_post_bp.route('/delete/<int:post_id>', methods=['POST'])
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('貼文已刪除。')
    return redirect(url_for('admin_post.post_list'))