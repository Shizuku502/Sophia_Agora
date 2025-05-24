from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.extensions import db
from app.models.comment import Comment
from app.utils.decorators import admin_required

admin_comment_bp = Blueprint(
    'admin_comment',
    __name__,
    url_prefix='/admin/comments',
    template_folder='templates/admin'  # 注意：這是相對於 app/admin 資料夾
)

@admin_comment_bp.route('/')
@admin_required
def comment_list():
    comments = Comment.query.all()
    return render_template('admin/manage_comment.html', comments=comments)

@admin_comment_bp.route('/delete/<int:comment_id>', methods=['POST'])
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('留言已刪除。')
    return redirect(url_for('admin_comment.comment_list'))