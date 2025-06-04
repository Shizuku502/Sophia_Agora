from app.extensions import db  # ← 正確地從 extensions 匯入 db

# 匯入所有 model，讓其他模組可以只匯入 models 使用全部
from app.models.user import User
from app.models.forbidden_word import Forbidden_Word
from app.models.post import Post
from app.models.comment import Comment
from app.models.reaction import Reaction
from app.models.notification import Notification
from app.models.post_edit_history import Post_Edit_History
from app.models.report import Report
from app.models.teacher import Teacher_Paper, Teacher_Experience, Teacher_Expertise
from app.models.teacher_available_schedule import Teacher_Available_Schedule
from app.models.teacher_schedule import Teacher_Schedule
from app.models.student_schedule import Student_Schedule 
from app.models.appointment import Appointment