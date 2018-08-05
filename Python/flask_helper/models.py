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
from sqlalchemy import Column, ForeignKey, Integer, String, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
#from app import app

__all__ = ('BEER_TYPES', 'Beer', 'Brewery', 'BeerPhotos', 'engine', 'Base')

BEER_TYPES = ['IPA Pilsner', 'Lager', 'Stoute Gose', 'Pale Ale', 'Ale', 'Saison',
    'Wheat Beer', 'Bock', 'Porter', 'Brown Ale', 'Pale Lager', 'Mild Ale',
    'Lambic', 'American Pale Ale', 'Irish Red Ale', 'American Lager', 'Amber Ale',
    'Cream Ale', 'Cider', 'Sour', 'Irish Stout', 'Malt', 'Blonde', 'Dark', 'Honey',
    'Fruit', 'Bitter', 'Kolsch', 'Hefeweizen', 'Double IPA', 'Oatmeal Stout']

# db path
db_path = os.path.join(os.path.dirname(thisDir), 'db').replace(os.sep, '/')
brewery_str = 'sqlite:///{}/beer.db'.format(db_path)

##db = SQLAlchemy(app)
##app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
##app.config['SQLALCHEMY_BINDS'] = {
##    'brewery': brewery_str
##}
##
##db.create_all(bind=['brewery'])
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

engine = create_engine(brewery_str)

