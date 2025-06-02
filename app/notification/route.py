# app/notification/route.py
from flask import Blueprint, jsonify, request, redirect, url_for, render_template, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.notification import Notification

notification_bp = Blueprint(
    "notification",
    __name__,
    url_prefix="/notification",
    template_folder="templates"
)

# 🔔 API：未讀通知詳細資料 + 未讀數量（for JS dropdown + 紅點）
@notification_bp.route("/api/unread")
@login_required
def api_unread_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False)\
        .order_by(Notification.created_at.desc()).all()

    data = [
        {
            "id": n.id,
            "content": n.content,
            "link": n.link,
            "created_at": n.created_at.isoformat(),  # 傳回 ISO 格式
            "is_read": n.is_read
        }
        for n in notifications
    ]
    return jsonify({
        "notifications": data,
        "unread_count": len(data)
    })


# 📬 JSON 通知列表（完整）
@notification_bp.route("/list")
@login_required
def list_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc()).all()
    return jsonify([
        {
            "id": n.id,
            "type": n.type,
            "content": n.content,
            "link": n.link,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat()  # 傳回 ISO 格式
        }
        for n in notifications
    ])


# 📄 HTML 通知列表頁面
@notification_bp.route("/view")
@login_required
def view_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc()).all()
    return render_template("notification/notification_list.html", notifications=notifications)


# ✅ 單一通知標記為已讀
@notification_bp.route("/mark-read/<int:notification_id>", methods=["POST"])
@login_required
def mark_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    notification.is_read = True
    db.session.commit()
    return jsonify({"status": "ok"})


# ✅ 一鍵標記所有通知為已讀
@notification_bp.route("/mark-all-read", methods=["POST"])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify({"status": "all read"})


# 🗑️ 刪除單一通知
@notification_bp.route("/delete/<int:notification_id>", methods=["POST"])
@login_required
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(notification)
    db.session.commit()
    return jsonify({"status": "deleted"})


# 🗑️ 一鍵清除所有通知
@notification_bp.route("/clear-all", methods=["POST"])
@login_required
def clear_all():
    Notification.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return redirect(url_for("notification.view_notifications"))


# 🕊️ 點擊通知 → 標記已讀 → 導向原始連結
@notification_bp.route("/go/<int:notification_id>")
@login_required
def go_and_mark(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        abort(403)
    notification.is_read = True
    db.session.commit()
    return redirect(notification.link or url_for('notification.list_notifications'))


# 🔢 🔥 新增：只回傳未讀通知數
@notification_bp.route("/unread-count")
@login_required
def unread_count():
    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({"unread": count})
