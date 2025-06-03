# utils/decorators.py

from functools import wraps
from flask import abort
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

# ✅ 管理員限定
def admin_required(f):
    """檢查使用者是否為管理員"""
    return require_role("admin")(f)

# ✅ 教師限定
def teacher_required(f):
    """檢查使用者是否為教師"""
    return require_role("teacher")(f)

# ✅ 你可以根據需要再加入 student_required
def student_required(f):
    """檢查使用者是否為學生"""
    return require_role("student")(f)

# 設定可匯出的函式
__all__ = ["require_role", "admin_required", "teacher_required", "student_required"]
