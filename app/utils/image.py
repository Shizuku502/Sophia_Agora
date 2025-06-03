# .utils/image.py

from PIL import Image

def compress_and_save_image(image_file, save_path, max_size=(500, 500), quality=85):
    """
    壓縮並儲存圖片。

    :param image_file: 傳入的檔案物件（form.avatar.data）
    :param save_path: 要儲存的完整路徑（含副檔名）
    :param max_size: 圖片最大尺寸（預設 500x500）
    :param quality: 儲存品質（預設 85）
    """
    image = Image.open(image_file)
    image = image.convert('RGB')
    image.thumbnail(max_size)
    image.save(save_path, optimize=True, quality=quality)