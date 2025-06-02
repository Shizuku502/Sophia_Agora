# utils/helpers.py

import re
from app.models.forbidden_word import Forbidden_Word

def get_forbidden_words():
    return [fw.word for fw in Forbidden_Word.query.all()]

def sanitize_content(content):
    words = get_forbidden_words()
    for word in words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        content = pattern.sub('*' * len(word), content)
    return content

def get_report_target_description(report):
    if report.reported_post:
        return f"貼文 #{report.reported_post_id}"
    elif report.reported_comment:
        return f"留言 #{report.reported_comment_id}"
    elif report.reported_user:
        return f"使用者 {report.reported_user.nickname or report.reported_user.username}"
    else:
        return "未知對象"
