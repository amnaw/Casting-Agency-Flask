#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#


# Associative table M-M relationship   
movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

# Roles table - Associative table M-M relationship     
actor_movies = db.Table('role',
    db.Column('actor_id', db.Integer, db.ForeignKey('Actor.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'), primary_key=True),
    db.Column('role', db.String)
)

# Associative table M-M relationship     
director_movies = db.Table('role',
    db.Column('director_id', db.Integer, db.ForeignKey('Director.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'), primary_key=True)
)

# Associative table M-M relationship 
director_genres = = db.Table('directo_genres',
    db.Column('directo_id', db.Integer, db.ForeignKey('Directo.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)




class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
   
    # Relationship with Movie - M-M
    movies = db.relationship('Movie', secondary=actor_movies,
      backref=db.backref('actors', lazy = 'joined', 
                                   cascade="all",
                                   passive_deletes=True))
    
    # methods to serialize model data
    # helper methods to simplify API behavior as insert
    def __init__(self, first_name, last_name, gender):
      self.first_name = first_name
      self.last_name = last_name
      self.gender = gender

    def insert(self):
      db.session.add(self)
      db.session.commit()
  
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
      return {
        'id': self.id,
        'name': self.first_name + " " + self.last_name,
        'gender': self.gender
        }




class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    rank = db.Column(db.Float, nullable=False)
    

    # Relationship with Genres - M-M
    genres = db.relationship('Genre', secondary=movie_genres,
      backref=db.backref('artists', lazy = 'joined',
                                   cascade="all",
                                   passive_deletes=True))
    
    def __init__(self, title, release_date, rank):
      self.title = title
      self.release_date = release_date
      self.rank = rank

    def insert(self):
      db.session.add(self)
      db.session.commit()
  
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
      return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date,
        'rank': self.rank
        }

      

class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String())

    def __init__(self, genre):
      self.genre = genre

    def insert(self):
      db.session.add(self)
      db.session.commit()
  
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()


class Assistant(db.Model):
    __tablename__ = 'Assistant'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    director_id = db.Column(db.Integer,db.ForeignKey('Director.id'), nullable=True)

    def __init__(self, first_name, last_name, director_id):
      self.first_name = first_name
      self.last_name = last_name
      self.director_id = director_id

    def insert(self):
      db.session.add(self)
      db.session.commit()
  
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
      return {
        'id': self.id,
        'name': self.first_name + " " + self.last_name,
        'director_id': self.director_id
        }


class Director(db.Model):
    __tablename__ = 'Director'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
   
    # Relationship with Movie - M-M
    movies = db.relationship('Movie', secondary=director_movies,
      backref=db.backref('directors', lazy = 'joined', 
                                   cascade="all",
                                   passive_deletes=True))

    # Relationship with Genre - M-M
    genres = db.relationship('Genre', secondary=director_genres,
      backref=db.backref('directors', lazy = 'joined',
                                   cascade="all",
                                   passive_deletes=True))

    # Relationship with Assistant - 1-M
    assistants =  db.relationship('Assistant', backref='director', lazy=True)

    def __init__(self, first_name, last_name):
      self.first_name = first_name
      self.last_name = last_name

    def insert(self):
      db.session.add(self)
      db.session.commit()
  
    def update(self):
      db.session.commit()

    def delete(self):
      db.session.delete(self)
      db.session.commit()

    def format(self):
      return {
        'id': self.id,
        'name': self.first_name + " " + self.last_name
        }

    


