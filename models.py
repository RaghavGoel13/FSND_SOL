# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

# For Local testing
database_path = 'postgresql://postgres:admin@localhost:5432/postgres'
# database_path = os.environ['DATABASE_URL']
if database_path[:10] != 'postgresql':
    database_path = database_path.replace('postgres', 'postgresql')
print(database_path)

db = SQLAlchemy()


# ----------------------------------------------------------------------------#
# HELPER METHOD TO SETUP DB
# ----------------------------------------------------------------------------#
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Actors(db.Model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(String(120), nullable=False)
    gender = Column(String(120), nullable=False)
    phone = Column(String(10), nullable=False)
    movie_id = Column(Integer, ForeignKey('Movies.id'), nullable=True)

    def __init__(self, name, gender, age, phone, movie_id):
        self.name = name
        self.gender = gender
        self.age = age
        self.phone = phone
        self.movie_id = movie_id

    def add_actor(self):
        db.session.add(self)
        db.session.commit()

    def update_actor(self):
        db.session.commit()

    def delete_actor(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def get_actor(self):
        return {'id': self.id,
                'name': self.name,
                'gender': self.gender,
                'age': self.age,
                'phone': self.phone,
                'movie_id': self.movie_id
                }


class Movies(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    rating = Column(Integer, nullable=False, default=False)
    release_date = Column(DateTime, nullable=False)
    actors = relationship('Actors', backref="Movies", lazy=True)

    def __init__(self, title, release_date, rating):
        self.title = title
        self.release_date = release_date
        self.rating = rating

    def add_movie(self):
        db.session.add(self)
        db.session.commit()

    def update_movie(self):
        db.session.commit()

    def delete_movie(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def get_movie(self):
        return {'id': self.id,
                'title': self.title,
                'release_date': self.release_date,
                'rating': self.rating,
                'actors': list(map(lambda actors: actors.get_actor, self.actors))
                }
