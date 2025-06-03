# 啟動應用

from app import create_app
from app.models import User, Forbidden_Word, Post, Comment, Reaction, Notification, Post_Edit_History, Report, Teacher_Paper, Teacher_Experience, Teacher_Expertise

app = create_app("app.config.DevelopmentConfig")
print("Registered Blueprints:", app.blueprints.keys())

if __name__ == "__main__":
    app.run(debug=True)