from datetime import datetime
import re
from markupsafe import Markup

def format_datetime(value, format="%Y-%m-%d %H:%M:%S"):
    if value is None:
        return ""  # 或者 return "N/A"
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return value.strftime(format)



def censor_text(text, forbidden_words=None, replace_char="*"):
    if forbidden_words is None:
        forbidden_words = ["敏感詞1", "敏感詞2", "不適當字詞"]
    for word in forbidden_words:
        pattern = re.compile(rf"{word}", re.IGNORECASE)
        text = pattern.sub(replace_char * len(word), text)
    return text

def utc_span(value):
    """
    將 datetime 格式轉為帶有 data-utc 的 span 元素，供 JavaScript 用戶端轉換為本地時間。
    :param value: datetime 類型
    :return: HTML span 元素 (包含 class="utc-time" 和 data-utc)
    """
    if isinstance(value, datetime):
        iso_utc = value.strftime('%Y-%m-%dT%H:%M:%SZ')  # UTC ISO 格式
        return Markup(f'<span class="utc-time" data-utc="{iso_utc}">{iso_utc}</span>')
    return value

# 設定可匯出的函式
__all__ = ["format_datetime", "censor_text", "utc_span"]

