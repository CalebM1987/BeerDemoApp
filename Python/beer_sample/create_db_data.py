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
print(os.path.join(os.path.dirname(thisDir), 'app', 'lib'))
sys.path.append(os.path.dirname(thisDir))
sys.path.append(os.path.join(os.path.dirname(thisDir), 'app', 'lib'))
import munch
import restapi
from app import models
#import models
reload(models)
from app.models import Beer, Brewery, BeerPhotos, Category, Style, session
from datetime import datetime
import csv

# url to AGOL layer with MN Brewery info
url = 'https://services2.arcgis.com/ZkOsbg84o8DsPPaP/arcgis/rest/services/Minnesota_Beer/FeatureServer/0'

timestamp_to_date = lambda s: datetime.strptime(s,'%Y-%m-%d %H:%M:%S UTC')

def get_mankato_beers():
    photo_dir = os.path.join(thisDir, 'photos')
    beers_json = os.path.join(thisDir, 'beers-mankato.json')

    with open(beers_json, 'r') as f:
        data = json.load(f)

        # return generator with beer info
        for beer in data:

            # beer obj
            photo_name = beer.get('photo')
            beerObj = munch.munchify({k: v for k,v in six.iteritems(beer) if k != 'photo'})
            beerObj.photo_name = photo_name

            # read photo as binary
            photo_path = os.path.join(photo_dir, photo_name)
            with open(photo_path, 'rb') as p:
                yield (beerObj, p.read())


def create_data():

    # create feature layer from service
    # lyr = restapi.FeatureLayer(url)
    #
    # # query
    # fs = lyr.query(outSR=4326)
    #
    # # iterate through query results and add to db
    # for feature in fs:
    #
    #     # add new brewery
    #     ft = feature.attributes
    #     newBrewery = Brewery(
    #         name=restapi.rest_utils.fix_encoding(ft.Name),
    #         county=ft.COUNTY,
    #         city=ft.CITY,
    #         address=ft.ADDRESS,
    #         monday=ft.MONDAY,
    #         tuesday=ft.TUESDAY,
    #         wednesday=ft.WEDNESDAY,
    #         thursday=ft.THURSDAY,
    #         friday=ft.FRIDAY,
    #         saturday=ft.SATURDAY,
    #         sunday=ft.SUNDAY,
    #         comments=ft.NOTES,
    #         brew_type=ft.TYPE,
    #         website=ft.Website,
    #         x=feature.geometry.x,
    #         y=feature.geometry.y
    #     )
    #
    #     # add mankato beers sample data if brewery is Mankato Brewery
    #     if newBrewery.name == 'Mankato Brewery':
    #         for beer, photoBlob in get_mankato_beers():
    #
    #             # create new beer first
    #             photo_name = beer.photo_name
    #             del beer.photo_name
    #             newBeer = Beer(**beer)
    #
    #             # create new beer photo
    #             newBeer.photos.append(BeerPhotos(photo_name=photo_name, data=photoBlob))
    #             newBrewery.beers.append(newBeer)
    #
    #     print('new brewery: ', newBrewery)
    #
    #     # add to session manager
    #     session.add(newBrewery)

    # test child
    # newBrewery.beers.append(Beer(name='test beer'))

    # load categories and styles
    categories = os.path.join(thisDir, 'categories.csv')
    styles = os.path.join(thisDir, 'styles.csv')
    # with open(categories, 'r') as csvfile:
    #     for row in list(iter(csv.reader(csvfile)))[1:]:
    #         # print row
    #         vals = row[:-1] + [timestamp_to_date(row[-1])]
    #         print vals, len(vals)
    #
    #         # category = Category(*row[1:-1] + [timestamp_to_date(row[-1])])
    #         category = Category(*vals)
    #         session.add(category)

    with open(styles, 'r') as csvfile:
        for row in list(iter(csv.reader(csvfile)))[1:]:

            print row
            ts = timestamp_to_date(row[-1])
            print ts
            style = Style(*row[:-1] + [ts])
            print row, len(row)
            session.add(style)

    # commit db changes
    session.commit()
    return session


if __name__ == '__main__':
    sesseion = create_data()
