# app/forum/reaction.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.reaction import Reaction

reaction_bp = Blueprint("reaction", __name__, url_prefix="/reactions")

@reaction_bp.route("/add", methods=["POST"])
@login_required
def add_reaction():
    post_id = request.json.get("post_id")
    comment_id = request.json.get("comment_id")
    reaction_type = request.json.get("type")

    # 先查詢是否已存在此使用者的回應
    existing = Reaction.query.filter_by(
        user_id=current_user.id,
        post_id=post_id,
        comment_id=comment_id
    ).first()

    if existing:
        if existing.type == reaction_type:
            # 已經按過同一個反應，則取消
            db.session.delete(existing)
            db.session.commit()
            return jsonify({"status": "removed"})
        else:
            # 改變反應種類
            existing.type = reaction_type
            db.session.commit()
            return jsonify({"status": "updated"})
    else:
        # 新增反應
        reaction = Reaction(
            type=reaction_type,
            user_id=current_user.id,
            post_id=post_id,
            comment_id=comment_id
        )
        db.session.add(reaction)
        db.session.commit()
        return jsonify({"status": "added"})