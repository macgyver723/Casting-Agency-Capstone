import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


class DatabaseItem():
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Movie(db.Model, DatabaseItem):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    genre = db.Column(db.String(150), nullable=False)
    # add a relationship to role

    def __repr__(self):
        return f"<Movie {self.id} {self.title} " \
            "Release date: {self.release_date} genres: {self.genre}>"


class Actor(db.Model, DatabaseItem):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    seeking_work = db.Column(db.Boolean, nullable=False, default=True)
    # add a relationship to role

    def get_age(self):
        age_in_seconds = (datetime.utcnow() - self.birthdate).total_seconds()
        return int(age_in_seconds / (60*60*24*365))

    def __repr__(self):
        return f"<Actor {self.id} Name: {self.name} Age: {self.get_age()} Gender: {self.gender} Seeking Work: {self.seeking_work}>"
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.get_age(),
            'gender': self.gender,
            'seeking_work': self.seeking_work
        }


'''
@TODO: complete this child table of Movie and Actor
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
'''
