# add_admin.py

from getpass import getpass
from app import create_app, db
from app.models import User

# 建立 Flask 應用程式
app = create_app()

with app.app_context():
    print("🔐 新增管理員帳號")
    
    account_id = input("請輸入管理者帳號：").strip()
    if not account_id:
        print("⚠️  帳號不能為空")
        exit()

    password = getpass("請輸入密碼（輸入時不會顯示）：").strip()
    if not password:
        print("⚠️  密碼不能為空")
        exit()

    # 確認帳號是否已存在
    existing_user = User.query.filter_by(account_id=account_id).first()
    if existing_user:
        print("❌ 該帳號已存在，請使用其他帳號。")
    else:
        # 建立新使用者
        new_user = User(
            account_id=account_id,
            role="admin",
            status="online"
        )
        new_user.set_password(password)  # 使用正確的設定密碼方式
        db.session.add(new_user)
        db.session.commit()
        print("✅ 管理員帳號建立成功！")
