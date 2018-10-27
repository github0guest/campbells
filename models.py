from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class Comic(db.Model):
    __tablename__ = 'comic'
    date = db.Column(db.Integer, primary_key=True)
    transcript = db.Column(db.Text)


class SearchTranscripts(db.Model):
    __tablename__ = 'search_transcripts'
    transcript = db.Column(db.Text)
    date = db.Column(db.Integer, primary_key=True)


if __name__ == '__main__':
    pass
