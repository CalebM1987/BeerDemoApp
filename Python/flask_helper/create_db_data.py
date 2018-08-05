#-------------------------------------------------------------------------------
# Name:        module1
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
import json
import six
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'lib'))
from munch import munchify
import restapi
import models
reload(models)
from models import Beer, Brewery, BeerPhotos, engine, Base
from sqlalchemy.orm import sessionmaker


# url to AGOL layer with MN Brewery info
url = 'https://services2.arcgis.com/ZkOsbg84o8DsPPaP/arcgis/rest/services/Minnesota_Beer/FeatureServer/0'

def get_mankato_beers():
    data_folder = os.path.join(os.path.dirname(thisDir), 'db', 'beer_sample')
    photo_dir = os.path.join(data_folder, 'photos')
    beers_json = os.path.join(data_folder, 'beers-mankato.json')

    with open(beers_json, 'r') as f:
        data = json.load(f)

        # return generator with beer info
        for beer in data:

            # beer obj
            photo_name = beer.get('photo')
            beerObj = munchify({k: v for k,v in six.iteritems(beer) if k != 'photo'})
            beerObj.photo_name = photo_name

            # read photo as binary
            photo_path = os.path.join(photo_dir, photo_name)
            with open(photo_path, 'rb') as p:
                yield (beerObj, p.read())


def create_data():
    # create tables
    Base.metadata.create_all(engine)

    # bind session to engine
    print('engine is: ', engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # make sure tables are clear
##    Breweries.query.delete()
##    Beers.query.delete()

    # create feature layer from service
    lyr = restapi.FeatureLayer(url)

    # query
    fs = lyr.query()

    # iterate through query results and add to db
    for feature in fs:

        # add new brewery
        ft = feature.attributes
        newBrewery = Brewery(
            name=restapi.rest_utils.fix_encoding(ft.Name),
            county=ft.COUNTY,
            city=ft.CITY,
            address=ft.ADDRESS,
            monday=ft.MONDAY,
            tuesday=ft.TUESDAY,
            wednesday=ft.WEDNESDAY,
            thursday=ft.THURSDAY,
            friday=ft.FRIDAY,
            saturday=ft.SATURDAY,
            sunday=ft.SUNDAY,
            comments=ft.NOTES,
            brew_type=ft.TYPE,
            website=ft.Website,
            x=feature.geometry.x,
            y=feature.geometry.y
        )

        # add mankato beers sample data if brewery is Mankato Brewery
        if newBrewery.name == 'Mankato Brewery':
            for beer, photoBlob in get_mankato_beers():

                # create new beer first
                photo_name = beer.photo_name
                del beer.photo_name
                newBeer = Beer(**beer)

                # create new beer photo
                newBeer.photos.append(BeerPhotos(photo_name=photo_name, data=photoBlob))
                newBrewery.beers.append(newBeer)

        print('new brewery: ', newBrewery)

        # add to session manager
        session.add(newBrewery)

    # test child
    # newBrewery.beers.append(Beer(name='test beer'))

    # commit db changes
    session.commit()
    return session



if __name__ == '__main__':
    sesseion = create_data()
