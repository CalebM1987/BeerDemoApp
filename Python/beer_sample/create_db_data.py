import os
import sys
import json
import six
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(thisDir))
import munch
import restapi
from app import models
reload(models)
from app.models import Beer, Brewery, BeerPhotos, Category, Style, session
from app.security import userStore
from datetime import datetime
import csv

# url to AGOL layer with MN Brewery info
url = 'https://services2.arcgis.com/ZkOsbg84o8DsPPaP/arcgis/rest/services/Minnesota_Beer/FeatureServer/0'

# function get utc time string to datetime()
timestamp_to_date = lambda s: datetime.strptime(s,'%Y-%m-%d %H:%M:%S UTC')


def get_mankato_beers():
    """generator to popuplate beers from mankato brewery
    :return:
    """
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


def load_csv(table, csv_file):
    """loads a csv into a database table, must share the same schema.

    :param table: sqlalchemy.Base Table object
    :param csv_file: path to csv file
    :return: None
    """
    with open(csv_file, 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            # convert date string to datetime() object
            row['last_mod'] = timestamp_to_date(row['last_mod'])

            # write row, unpack dict to key word arguments
            record = table(**row)
            session.add(record)


def create_data():
    """ creates the necessary base data for workshop demo """

    # create feature layer from service
    lyr = restapi.FeatureLayer(url)

    # query
    fs = lyr.query(outSR=4326)

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

    # load categories and styles
    categories = os.path.join(thisDir, 'categories.csv')
    styles = os.path.join(thisDir, 'styles.csv')

    # call our function to load data to SQLite
    load_csv(Category, categories)
    load_csv(Style, styles)

    # commit db changes
    session.commit()

    # create test_user
    user = userStore.create_user('John Doe', 'test_user@gmail.com', 'test_user', 'user123', activated='True')
    print('created test user: {}'.format(user))


if __name__ == '__main__':

    # run function to create the data
    create_data()
