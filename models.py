import os
from sqlalchemy import Column, String, Integer, Boolean
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# database_name = "tristan"
# db_user = os.environ['DB_USER']
# db_pass = os.environ['DB_PASS']
database_path = os.environ['DATABASE_URL']


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Game(db.Model):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String(500))

    release_date = Column(String)
    released = Column(Boolean)

    rating = Column(Integer)
    critic_rating = Column(Integer)
    PEGI_rating = Column(Integer)

    genres = Column(String)
    developer = Column(String)
    publisher = Column(String)

    def __init__(self, name, description, release_date, released, rating,
                 critic_rating, PEGI_rating, genres, developer, publisher):
        self.name = name
        self.description = description
        self.release_date = release_date
        self.released = released
        self.rating = rating
        self.critic_rating = critic_rating
        self.PEGI_rating = PEGI_rating
        self.genres = genres
        self.developer = developer
        self.publisher = publisher

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Developer(db.Model):
    __tablename__ = 'Developer'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String(500))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class publisher(db.Model):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String(500))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
