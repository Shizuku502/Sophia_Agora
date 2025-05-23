# app/auth/routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from datetime import datetime

from app.extensions import db, login_manager
from app.models.user import User

auth_bp = Blueprint("auth", __name__, template_folder="templates")

# 設定登入用的用戶加載器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_account = request.form["account_id"].strip()
        input_password = request.form["password"]
        print(f"輸入帳號：{user_account}")

        user = User.query.filter_by(account_id=user_account).first()

        if not user:
            print("查無此帳號")
            return render_template("auth/login.html", errorMsg="查無帳號")
        if not check_password_hash(user.password, input_password):
            return render_template("auth/login.html", errorMsg="密碼錯誤")

        # 更新最後登入時間並登入
        user.last_login = datetime.now()
        db.session.commit()
        login_user(user)

        return redirect(url_for("forum.index"))  # 假設登入後導向論壇首頁

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))