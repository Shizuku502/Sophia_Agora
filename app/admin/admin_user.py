from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.extensions import db
from app.models.user import User
from app.utils.decorators import admin_required

admin_user_bp = Blueprint('admin_user', __name__, url_prefix='/admin/users')

@admin_user_bp.route('/')
@admin_required
def user_list():
    users = User.query.all()
    return render_template('admin/manage_user.html', users=users)

@admin_user_bp.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('使用者已刪除。')
    return redirect(url_for('admin_user.user_list'))

@admin_user_bp.route('/toggle-role/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user_role(user_id):
    user = User.query.get_or_404(user_id)

    # 只切換 admin 與 student（或依據你支援的角色調整）
    if user.role == 'admin':
        user.role = 'student'
        flash("已降級為一般使用者。")
    else:
        user.role = 'admin'
        flash("已升級為管理員。")

    db.session.commit()
    return redirect(url_for('admin_user.user_list'))

@admin_user_bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        account_id = request.form.get('account_id')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        role = request.form.get('role')

        if not account_id or not password:
            flash("帳號與密碼為必填", "error")
            return redirect(url_for('admin_user.add_user'))

        if User.query.filter_by(account_id=account_id).first():
            flash("帳號已存在", "error")
            return redirect(url_for('admin_user.add_user'))

        new_user = User(
            account_id=account_id,
            nickname=nickname or "未設定",
            role=role
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash("使用者已新增")
        return redirect(url_for('admin_user.user_list'))

    return render_template('admin/add_user.html')
