#-------------------------------------------------------------------------------
# Name:        models.py
# Purpose:
#
# Author:      calebma
#
# Created:     03/08/2018
# Copyright:   (c) calebma 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'lib'))
from datetime import datetime, timedelta
from sqlalchemy import Column, ForeignKey, Integer, String, Float, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
# from SQLAlchemy.pool import SingletonThreadPool
from flask_login import UserMixin

__all__ = ('BEER_TYPES', 'Beer', 'Brewery', 'BeerPhotos', 'engine', 'Base')

BEER_TYPES = ['IPA Pilsner', 'Lager', 'Stoute Gose', 'Pale Ale', 'Ale', 'Saison',
    'Wheat Beer', 'Bock', 'Porter', 'Brown Ale', 'Pale Lager', 'Mild Ale',
    'Lambic', 'American Pale Ale', 'Irish Red Ale', 'American Lager', 'Amber Ale',
    'Cream Ale', 'Cider', 'Sour', 'Irish Stout', 'Malt', 'Blonde', 'Dark', 'Honey',
    'Fruit', 'Bitter', 'Kolsch', 'Hefeweizen', 'Double IPA', 'Oatmeal Stout']

# db path
db_path = os.path.join(os.path.dirname(thisDir), 'db').replace(os.sep, '/')
brewery_str = 'sqlite:///{}/beer2.db'.format(db_path)

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

# is_authenticated
# This property should return True if the user is authenticated, i.e. they have provided valid credentials. (Only authenticated users will fulfill the criteria of login_required.)
# is_active
# This property should return True if this is an active user - in addition to being authenticated, they also have activated their account, not been suspended, or any condition your application has for rejecting an account. Inactive accounts may not log in (without being forced of course).
# is_anonymous
# This property should return True if this is an anonymous user. (Actual users should return False instead.)
# get_id()
# This method must return a unicode that uniquely identifies this user, and can be used to load the user from the user_loader callback. Note that this must be a unicode - if the ID is natively an int or some other type, you will need to convert it to unicode.

class Users(Base, UserMixin):
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
        return self.activated == 'True'

    def __repr__(self):
        return '<User: "{}">'.format(self.username)

    def __str__(self):
        return repr(self)

    # @property
    # def is_authenticated(self):
    #     return True
    #
    # @property
    # def is_active(self):
    #     return True
    #
    # @property
    # def is_anonymous(self):
    #     return False
    #
    # def get_id(self):
    #     return self.id


engine = create_engine(brewery_str)#, poolclass=SingletonThreadPool)