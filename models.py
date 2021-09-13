from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Genre_Game(db.Model):
    __tablename__ = 'Genre_Game'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('Genre.id'))


class Game(db.Model):
    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    description = db.Column(db.String(500))

    release_date = db.Column(db.DateTime)
    released = db.Column(db.Boolean)

    rating = db.Column(db.Integer)
    critic_rating = db.Column(db.Integer)
    PEGI_rating = db.Column(db.Integer)

    genres = db.relationship(
        'Genre_Game', backref='mygenres', cascade="all, delete")
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


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
