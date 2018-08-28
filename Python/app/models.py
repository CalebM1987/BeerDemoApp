import os
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_login import UserMixin

__all__ = ('Beer', 'Brewery', 'BeerPhotos', 'User', 'Category', 'Style', 'engine', 'Base', 'session')

# db path, make sure "check_same_thread" is set to False
thisDir = os.path.dirname(__file__)
db_path = os.path.join(os.path.dirname(thisDir), 'db').replace(os.sep, '/')
brewery_str = 'sqlite:///{}/beer.db?check_same_thread=False'.format(db_path)

# get declaritive base context
Base = declarative_base()

class BeerPhotos(Base):
    __tablename__ = 'beer_photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    beer_id = Column(Integer, ForeignKey('beers.id'))
    photo_name = Column(String(100))
    data = Column(LargeBinary)

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
    brewery = relationship('Brewery', back_populates='beers')

    def __repr__(self):
        return '<Beer: "{}" ({})>'.format(self.name, self.style)


class Brewery(Base):
    __tablename__ = 'breweries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    county = Column(String(3))
    city = Column(String(50))
    address = Column(String(100))
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
    beers = relationship('Beer', back_populates='brewery')

    def __repr__(self):
        return '<Brewery: "{}">'.format(self.name)

class Style(Base):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_id = Column(Integer, ForeignKey('categories.id'))
    style_name = Column(String(100), nullable=False)
    last_mod = Column(DateTime, default=datetime.utcnow())
    category = relationship('Category', back_populates='styles')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_name = Column(String(100), nullable=False)
    last_mod = Column(DateTime, default=datetime.utcnow())
    styles = relationship('Style', back_populates='category')

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
    activated = Column(String(5), default='False')

    @property
    def is_active(self):
        """ override UserMixin.is_active property """
        return self.activated == 'True'

    def __repr__(self):
        return '<User: "{}">'.format(self.username)

    def __str__(self):
        return repr(self)

# make sure all databases are created
engine = create_engine(brewery_str)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
