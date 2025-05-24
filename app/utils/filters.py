from datetime import datetime
import re

def format_datetime(value, format="%Y-%m-%d %H:%M:%S"):
    """
    格式化日期時間
    :param value: datetime 或字串格式的日期
    :param format: 期望的格式 (預設: "YYYY-MM-DD HH:MM:SS")
    :return: 格式化後的日期時間字串
    """
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return value.strftime(format)

def censor_text(text, forbidden_words=None, replace_char="*"):
    """
    過濾敏感詞並替換為特殊符號
    :param text: 要檢查的文字
    :param forbidden_words: 敏感詞清單
    :param replace_char: 替換用的字符 (預設: "*")
    :return: 處理後的文字
    """
    if forbidden_words is None:
        forbidden_words = ["敏感詞1", "敏感詞2", "不適當字詞"]  # 可以自訂黑名單

    for word in forbidden_words:
        pattern = re.compile(rf"\b{word}\b", re.IGNORECASE)
        text = pattern.sub(replace_char * len(word), text)

    return text

# 設定可匯出的函式
__all__ = ["format_datetime", "censor_text"]
