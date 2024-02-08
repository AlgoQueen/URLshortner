from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String(1000), nullable=False)
    short = db.Column(db.String(100), primary_key=True, nullable=False)
