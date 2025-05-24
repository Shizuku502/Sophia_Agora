# app/forum/reaction.py

from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.reaction import Reaction

reaction_bp = Blueprint("reaction", __name__, url_prefix="/reactions")

@reaction_bp.route("/add", methods=["POST"])
@login_required
def add_reaction():
    post_id = request.form.get("post_id")
    comment_id = request.form.get("comment_id")
    reaction_type = request.form["type"]

    reaction = Reaction(type=reaction_type, user_id=current_user.id)

    if post_id:
        reaction.post_id = int(post_id)
    elif comment_id:
        reaction.comment_id = int(comment_id)
    else:
        flash("沒有指定對象", "danger")
        return redirect(request.referrer)

    db.session.add(reaction)
    db.session.commit()
    flash("你已成功表態")
    return redirect(request.referrer)