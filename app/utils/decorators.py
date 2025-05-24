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

# ✅ 新增 admin_required 裝飾器
def admin_required(f):
    """檢查使用者是否為管理員"""
    return require_role("admin")(f)  # 直接使用 require_role 來限制管理員存取

# 設定可匯出的函式
__all__ = ["require_role", "admin_required"]
