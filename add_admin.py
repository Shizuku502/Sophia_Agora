# add_admin.py

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# 初始化 Flask app context
app = create_app()

with app.app_context():
    account_id = input("請輸入管理者帳號：")
    password = input("請輸入密碼：")
    role = "admin"

    # 檢查帳號是否已存在
    existing_user = User.query.filter_by(account_id=account_id).first()
    if existing_user:
        print(" 帳號已存在，請使用不同帳號。")
    else:
        new_user = User(
            account_id=account_id,
            password=generate_password_hash(password),
            role="admin",      #設定角色
            status="active"    #可選:啟用狀態
        )
        db.session.add(new_user)
        db.session.commit()
        print("管理者帳號建立成功！")
