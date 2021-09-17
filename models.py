import os
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# database_name = "tristan"
# db_user = os.environ['DB_USER']
# db_pass = os.environ['DB_PASS']
# database_path = os.environ['DATABASE_URL']
dev_database_path = database_path = "postgresql://postgres:gsaiho2017@localhost:5432/tristan"
prod_database_path = 'postgresql://ebulgcmkogfscf:d516f4d3a4f3ece5f8710ac6ebc9be05fbaec90b226932ecb2b9b15044abbe58@ec2-18-215-44-132.compute-1.amazonaws.com:5432/d2n6j67332m9ll'


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = dev_database_path
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
