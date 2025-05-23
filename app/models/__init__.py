from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.forbidden_word import ForbiddenWord
from models.post import Post
from models.comment import Comment
from models.reaction import Reaction