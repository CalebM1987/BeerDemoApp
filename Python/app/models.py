import os
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_login import UserMixin
from datetime import timedelta

__all__ = ('Beer', 'Brewery', 'BeerPhotos', 'User', 'Category', 'Style', 'engine', 'Base', 'session')

# db path, make sure "check_same_thread" is set to False
thisDir = os.path.dirname(__file__)
db_path = os.path.join(os.path.dirname(thisDir), 'db').replace(os.sep, '/')
brewery_str = 'sqlite:///{}/beer.db?check_same_thread=False'.format(db_path)

# get declaritive base context
Base = declarative_base()

# basic repr
basic_repr = lambda obj, attr: '<{}: "{}">'.format(obj.__class__.__name__, getattr(obj, attr))

class BeerPhotos(Base):
    __tablename__ = 'beer_photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    beer_id = Column(Integer, ForeignKey('beers.id'))
    photo_name = Column(String(100))
    data = Column(LargeBinary)

    def __repr__(self):
        return basic_repr(self, 'photo_name')

class Beer(Base):
    __tablename__ = 'beers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brewery_id = Column(Integer, ForeignKey('breweries.id'))
    name = Column(String(150))
    description = Column(String(500))
    style = Column(String(50))
    alc = Column(Float)
    ibu = Column(Integer)
    color = Column(String(25))
    photos = relationship(BeerPhotos)
    created_by = Column(Integer, ForeignKey('users.id'))
    brewery = relationship('Brewery', back_populates='beers')
    user = relationship('User', back_populates='submitted_beers')

    def __repr__(self):
        return '<{}: "{}" ({})>'.format(self.__class__.__name__, self.name, self.style)


class Brewery(Base):
    __tablename__ = 'breweries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    address = Column(String(100))
    city = Column(String(50))
    state = Column(String(2))
    zip = Column(String(11))
    monday = Column(String(30))
    tuesday = Column(String(30))
    wednesday = Column(String(30))
    thursday = Column(String(30))
    friday = Column(String(30))
    saturday = Column(String(30))
    sunday = Column(String(30))
    comments = Column(String(255))
    brew_type = Column(String(50))
    website = Column(String(255))
    x = Column(Float)
    y = Column(Float)
    created_by = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='submitted_breweries')
    beers = relationship('Beer', back_populates='brewery')

    def __repr__(self):
        return basic_repr(self, 'name')

class Style(Base):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_id = Column(Integer, ForeignKey('categories.id'))
    style_name = Column(String(100), nullable=False)
    last_mod = Column(DateTime, default=datetime.utcnow())
    category = relationship('Category', back_populates='styles')

    def __repr__(self):
        return basic_repr(self, 'style_name')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_name = Column(String(100), nullable=False)
    last_mod = Column(DateTime, default=datetime.utcnow())
    styles = relationship('Style', back_populates='category')

    def __repr__(self):
        return basic_repr(self, 'cat_name')

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String(64))
    created = Column(DateTime, default=datetime.utcnow())
    last_login = Column(DateTime)
    expires = Column(DateTime, default=datetime.utcnow() + timedelta(hours=8))
    activated = Column(String(5), default='False')
    submitted_breweries = relationship('Brewery')
    submitted_beers = relationship('Beer')

    @property
    def is_active(self):
        """ override UserMixin.is_active property """
        return self.activated == 'True'

    def __repr__(self):
        return basic_repr(self, 'username')

    def __str__(self):
        return repr(self)

# make sure all databases are created
engine = create_engine(brewery_str)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()