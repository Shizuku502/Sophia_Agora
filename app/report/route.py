# app/report/route.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models.report import Report
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.notification import Notification
from app.utils.decorators import admin_required

report_bp = Blueprint("report", __name__, url_prefix='/report', template_folder='templates')


# 🔸 提交檢舉（通用，依 target_type 傳入）
@report_bp.route('/submit', methods=['POST'])
@login_required
def submit_report():
    target_type = request.form.get('target_type')
    target_id = request.form.get('target_id')
    reason = request.form.get('reason')

    if not reason or target_type not in ['user', 'post', 'comment']:
        return jsonify({'success': False, 'message': '請輸入有效檢舉事由與目標類型。'}), 400

    report = Report(
        reporter_id=current_user.id,
        reason=reason
    )

    if target_type == 'user':
        report.reported_user_id = target_id
    elif target_type == 'post':
        report.reported_post_id = target_id
    elif target_type == 'comment':
        report.reported_comment_id = target_id

    db.session.add(report)
    db.session.commit()

    # 通知所有管理員
    admins = User.query.filter_by(role='admin').all()
    for admin in admins:
        notif = Notification(
            user_id=admin.id,
            type='report',
            content=f"使用者 {current_user.display_name} 提出了一項檢舉。",
            link="/admin/report?only_pending=1"
        )
        db.session.add(notif)
    db.session.commit()

    return jsonify({'success': True, 'message': '檢舉已提交，等待管理員審核。'})