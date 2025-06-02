# .admin/admin_report.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models.user import User
from app.models.report import Report
from app.models.comment import Comment
from app.models.post import Post
from app.models.notification import Notification
from app.utils.decorators import admin_required
from app.utils.helpers import get_report_target_description

admin_report_bp = Blueprint('admin_report', __name__, url_prefix='/admin/report')


@admin_report_bp.route('/')
@admin_required
def report_list():
    page = request.args.get('page', 1, type=int)
    only_pending = request.args.get('only_pending') == '1'
    
    query = Report.query.order_by(Report.created_at.desc())
    if only_pending:
        query = query.filter_by(status='pending')

    pagination = query.paginate(page=page, per_page=10)
    reports = pagination.items

    # 預載相關資料避免 lazy loading
    for report in reports:
        report.reporter = User.query.get(report.reporter_id)
        report.reviewer = User.query.get(report.reviewer_id) if report.reviewer_id else None
        report.reported_user = User.query.get(report.reported_user_id) if report.reported_user_id else None
        report.reported_post = Post.query.get(report.reported_post_id) if report.reported_post_id else None
        report.reported_comment = Comment.query.get(report.reported_comment_id) if report.reported_comment_id else None

    return render_template('admin/report_list.html', reports=reports, pagination=pagination, only_pending=only_pending)


@admin_report_bp.route('/approve/<int:report_id>', methods=['POST'])
@admin_required
def approve_report(report_id):
    report = Report.query.get_or_404(report_id)
    if report.status != 'pending':
        return jsonify({'status': 'error', 'message': '該檢舉已處理'})

    reported_user = (
        report.reported_user or
        (report.reported_post.user if report.reported_post else None) or
        (report.reported_comment.user if report.reported_comment else None)
    )

    if reported_user:
        reported_user.deduct_points(5)

    report.status = 'approved'
    report.reviewer_id = current_user.id
    report.reviewed_at = datetime.utcnow()

    notification = Notification(
        user_id=report.reporter_id,
        type='system',
        content=f"您對「{get_report_target_description(report)}」的檢舉已通過，對方已被扣分。",
        link=None
    )
    db.session.add(notification)
    db.session.commit()

    return jsonify({'status': 'success', 'message': '已扣分並通知檢舉人'})


@admin_report_bp.route('/reject/<int:report_id>', methods=['POST'])
@admin_required
def reject_report(report_id):
    report = Report.query.get_or_404(report_id)
    if report.status != 'pending':
        return jsonify({'status': 'error', 'message': '該檢舉已處理'})

    report.status = 'rejected'
    report.reviewer_id = current_user.id
    report.reviewed_at = datetime.utcnow()

    notification = Notification(
        user_id=report.reporter_id,
        type='system',
        content=f"您對「{get_report_target_description(report)}」的檢舉已駁回",
        link=None
    )
    db.session.add(notification)
    db.session.commit()

    return jsonify({'status': 'success', 'message': '已忽略該檢舉並通知檢舉人'})


@admin_report_bp.route('/punish/<int:user_id>', methods=['POST'])
@admin_required
@login_required
def punish_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        points = int(request.form.get('points', 0))
    except ValueError:
        flash('扣分數值錯誤', 'danger')
        return redirect(url_for('admin_report.report_list'))

    if user.role != 'admin':
        user.deduct_points(points)
        db.session.commit()
        flash(f'已扣除 {user.display_name} {points} 分，目前剩餘 {user.points} 分。', 'success')
    else:
        flash('無法懲處管理員帳號。', 'danger')

    return redirect(url_for('admin_report.report_list'))
