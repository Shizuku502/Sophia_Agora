from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, BooleanField
from wtforms.validators import Optional
from flask_wtf.file import FileAllowed

class EditProfileForm(FlaskForm):
    nickname = StringField('暱稱', validators=[Optional()])
    avatar = FileField('上傳頭像', validators=[FileAllowed(['jpg', 'jpeg', 'png'], '只允許上傳圖片')])
    remove_avatar = BooleanField('移除現有頭像')
    submit = SubmitField('更新')