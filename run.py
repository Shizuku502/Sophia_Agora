# 啟動應用

from app import create_app
from app.models import User, ForbiddenWord, Post, Comment, Reaction

app = create_app()

if __name__ == '__main__':
    app.run(debug = True)