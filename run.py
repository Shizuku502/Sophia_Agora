# 啟動應用

from app import create_app
from app.models import User, Forbidden_Word, Post, Comment, Reaction, Notification

app = create_app("app.config.DevelopmentConfig")
print("Registered Blueprints:", app.blueprints.keys())

if __name__ == "__main__":
    app.run(debug=True)