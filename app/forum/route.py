# app/forum/route.py
from flask import Blueprint, render_template
from app.models.post import Post

forum_bp = Blueprint(
    "forum", __name__,
    url_prefix="/forum",
    template_folder="templates"  # ✅ 這一行是關鍵
)

@forum_bp.route("/")
def forum_home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("forum/index.html", posts=posts)
