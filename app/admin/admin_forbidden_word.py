from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.extensions import db
from app.models.forbidden_word import Forbidden_Word
from app.utils.decorators import admin_required

admin_forbidden_word_bp = Blueprint('admin_forbidden_word', __name__, url_prefix='/admin/forbidden')

@admin_forbidden_word_bp.route('/')
@admin_required
def forbidden_word_list():
    words = Forbidden_Word.query.order_by(Forbidden_Word.id.desc()).all()
    return render_template('admin/manage_forbidden_word.html', words=words)

@admin_forbidden_word_bp.route('/add_forbidden_word', methods=['GET', 'POST'])
@admin_required
def add_forbidden():
    if request.method == 'POST':
        word = request.form.get('word', '').strip()
        if not word:
            flash('請輸入禁用詞', 'warning')
            return redirect(url_for('admin_forbidden_word.forbidden_word_list'))

        existing = Forbidden_Word.query.filter_by(word=word).first()
        if existing:
            flash(f'禁用詞「{word}」已存在。', 'danger')
            return redirect(url_for('admin_forbidden_word.forbidden_word_list'))

        db.session.add(Forbidden_Word(word=word))
        db.session.commit()
        flash(f'已成功新增禁用詞：{word}', 'success')
        return redirect(url_for('admin_forbidden_word.forbidden_word_list'))

    return render_template('admin/add_forbidden_word.html')

@admin_forbidden_word_bp.route('/delete/<int:word_id>', methods=['POST'])
@admin_required
def delete_forbidden(word_id):
    word = Forbidden_Word.query.get_or_404(word_id)
    db.session.delete(word)
    db.session.commit()
    flash('禁用詞已刪除。')
    return redirect(url_for('admin_forbidden_word.forbidden_word_list'))

