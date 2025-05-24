from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def homepage():
    return render_template("homepage.html")

@main_bp.route("/teacher")
def teacher():
    return render_template("teacher.html")

@main_bp.route("/YiWen_Wang")
def YiWen_Wang():
    return render_template("YiWen_Wang.html")

@main_bp.route("/ChunHsiu_Yeh")
def ChunHsiu_Yeh():
    return render_template("ChunHsiu_Yeh.html")

@main_bp.route("/ChinSheng_Yu")
def ChinSheng_Yu():
    return render_template("ChinSheng_Yu.html")