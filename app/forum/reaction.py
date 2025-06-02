# app/forum/reaction.py

from flask import Blueprint, request, jsonify, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.reaction import Reaction

reaction_bp = Blueprint("reaction", __name__, url_prefix="/reactions")

@reaction_bp.route("/add", methods=["POST"])
@login_required
def add_reaction():
    if not current_user.can_participate():
        return jsonify({"error": "您的分數過低（須達 80 分），無法進行按讚或反對操作。"}), 403

    post_id = request.json.get("post_id")
    comment_id = request.json.get("comment_id")
    reaction_type = request.json.get("type")

    from app.models.post import Post
    from app.models.comment import Comment
    from app.models.notification import Notification

    is_post = post_id is not None
    target = Post.query.get(post_id) if is_post else Comment.query.get(comment_id)
    if not target:
        return jsonify({"error": "找不到目標內容"}), 404

    existing = Reaction.query.filter_by(
        user_id=current_user.id,
        post_id=post_id if is_post else None,
        comment_id=comment_id if not is_post else None
    ).first()

    if existing:
        if existing.type == reaction_type:
            db.session.delete(existing)
            db.session.commit()
            return jsonify({
                "status": "removed",
                "like_count": target.like_count,
                "dislike_count": target.dislike_count
            })
        else:
            existing.type = reaction_type
            db.session.commit()
            return jsonify({
                "status": "updated",
                "like_count": target.like_count,
                "dislike_count": target.dislike_count
            })

    reaction = Reaction(
        type=reaction_type,
        user_id=current_user.id,
        post_id=post_id if is_post else None,
        comment_id=comment_id if not is_post else None
    )
    db.session.add(reaction)
    db.session.flush()

    if target.user_id != current_user.id:
        title = target.title if is_post else target.content[:20] + "..."
        content_type = "文章" if is_post else "留言"
        notification = Notification(
            user_id=target.user_id,
            type=reaction_type,
            content=f"{current_user.nickname} 對你的{content_type}做出了反應《{title}》",
            link=url_for('post.post_detail', post_id=post_id if is_post else target.post_id)
        )
        db.session.add(notification)

    db.session.commit()
    return jsonify({
        "status": "added",
        "like_count": target.like_count,
        "dislike_count": target.dislike_count
    })
