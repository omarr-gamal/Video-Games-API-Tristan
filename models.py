from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    description = db.Column(db.String(500))

    release_date = db.Column(db.String)
    released = db.Column(db.Boolean)

    rating = db.Column(db.Integer)
    critic_rating = db.Column(db.Integer)
    PEGI_rating = db.Column(db.Integer)

    genres = db.Column(db.String)
    developer = db.Column(db.String)
    publisher = db.Column(db.String)


class Developer(db.Model):
    __tablename__ = 'Developer'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    description = db.Column(db.String(500))


class publisher (db.Model):
    __tablename__ = 'Publisher'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    description = db.Column(db.String(500))
