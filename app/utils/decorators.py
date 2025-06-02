# utils/decorators.py

from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user

def require_role(*roles):
    """檢查使用者是否擁有指定角色"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)  # 未登入則禁止存取
            if current_user.role not in roles:
                abort(403)  # 角色不符合則禁止存取
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ✅ 新增 admin_required 裝飾器
def admin_required(f):
    """檢查使用者是否為管理員"""
    return require_role("admin")(f)  # 直接使用 require_role 來限制管理員存取

# 設定可匯出的函式
__all__ = ["require_role", "admin_required"]

# 使用者行為限制
def check_user_score(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.score < 80 and not current_user.is_admin:
            flash("您的評分低於 80，無法使用此功能", "danger")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function