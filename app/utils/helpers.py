# utils/helpers.py

from app.models.forbidden_word import Forbidden_Word

def get_forbidden_words():
    return [fw.word for fw in Forbidden_Word.query.all()]

def sanitize_content(content):
    words = get_forbidden_words()
    for word in words:
        content = content.replace(word, "*" * len(word))
    return content