import os
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

environment = os.environ['ENVIRONMENT']
database_path = ''

if environment == 'dev':
    database_name = "tristan"
    db_user = os.environ['DB_USER']
    db_pass = os.environ['DB_PASS']
    database_path = "postgresql://{}:{}@{}/{}".format(db_user, db_pass,
                                                      'localhost:5432', database_name)
elif environment == 'prod':
    database_path = os.environ['DB_URL']


def setup_db(app):
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
    developer_id = Column(Integer, db.ForeignKey('Developer.id'))
    publisher_id = Column(Integer, db.ForeignKey('Publisher.id'))

    def __init__(self, name, description, release_date, released, rating,
                 critic_rating, PEGI_rating, genres, developer_id, publisher_id):
        self.name = name
        self.description = description
        self.release_date = release_date
        self.released = released
        self.rating = rating
        self.critic_rating = critic_rating
        self.PEGI_rating = PEGI_rating
        self.genres = genres
        self.developer_id = developer_id
        self.publisher_id = publisher_id

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

    developed_games = relationship("Game", backref='developed_games',
                                   cascade="all, delete")

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


class Publisher(db.Model):
    __tablename__ = 'Publisher'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String(500))

    published_games = relationship("Game", backref='published_games',
                                   cascade="all, delete")

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
