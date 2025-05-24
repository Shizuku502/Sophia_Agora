from flask import Blueprint, render_template, redirect, url_for, request, flash

admin_bp = Blueprint("admin_main", __name__, template_folder="templates")


@admin_bp.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")
