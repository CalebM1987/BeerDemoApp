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
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'lib'))
import restapi
import models
reload(models)
from models import Beers, Brewery, engine, Base
from sqlalchemy.orm import sessionmaker


# url to AGOL layer with MN Brewery info
url = 'https://services2.arcgis.com/ZkOsbg84o8DsPPaP/arcgis/rest/services/Minnesota_Beer/FeatureServer/0'

def create_data():
    # create tables
    Base.metadata.create_all(engine)

    # bind session to engine
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession

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
            name=ft.Name,
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
            style=ft.TYPE,
            website=ft.Website,
            x=feature.geometry.x,
            y=feature.geometry.y
        )

        # add to session manager
        session.add(newBrewery)

    # commit db changes
    session.commit()



if __name__ == '__main__':
    create_data()
