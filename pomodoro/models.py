from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.DateTime, nullable=False)
    finished_at = db.Column(db.DateTime, nullable=False)


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    work_minutes = db.Column(db.Integer, nullable=False, default=25)
    short_break_minutes = db.Column(db.Integer, nullable=False, default=5)
    long_break_minutes = db.Column(db.Integer, nullable=False, default=15)
    cycles_until_long_break = db.Column(db.Integer, nullable=False, default=4)
