from app.extensions import db

class Forbidden_Word(db.Model):
    __tablename__ = "forbidden_words"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<ForbiddenWord {self.word}>"