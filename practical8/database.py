from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.String(300), nullable=False)

    priority = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), nullable=False)

    due_date = db.Column(db.Date, nullable=False)