from flask import jsonify, Blueprint, request
from models import *
from sqlalchemy.orm import sessionmaker
from utils import *

Base.metadata.create_all(engine)

# bind session to engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# add brewery API blueprint
brewery_api = Blueprint('brewery_api', __name__)

# bind query method
Brewery.query = session.query(Brewery)
Beer.query = session.query(Beer)

# get list of brewery fields to use as default
brewery_fields = list_fields(Brewery)
beer_fields = list_fields(Beer)
beer_photo_fields = list_fields(BeerPhotos)
print(brewery_fields)

# toGeoJson() handler for results
def toGeoJson(d):
    if not isinstance(d, list):
        d = [d]
    return {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:EPSG::3857"
            }
        },
       "features": [
            {
                "type": "Feature",
                "properties": f,
                "geometry": {
                    "type": "Point",
                    "coordinates": [f.get('x'), f.get('y')]
                }
            } for f in d
        ]
    }

# constants
PHOTO_MIMETYPE = 'application/octet-stream'
ID_REQUIRED = {'error': {'code': 404, 'message': 'an ID is required'}}


# REST API METHODS BELOW

@brewery_api.route('/breweries')
@brewery_api.route('/breweries/<id>')
def get_breweries(id=None):
    args = collect_args()
    f = args.get('f', 'json')
    handler = toGeoJson if f.lower() == 'geojson' else lambda t: t
    fields = args.get('fields') or brewery_fields

    if id:
        brewery = query_wrapper(Brewery, id=int(id))
        return jsonify(handler(to_json(brewery, fields)))

    # query as normal
    results = query_wrapper(Brewery, **args)
    out_results = []
    for result in results:
        js = to_json(result, fields)
        out_results.append(js)
    return jsonify(handler(out_results))

@brewery_api.route('/breweries/<id>/beers')
def get_beers_from_brewery(id=None):
    if not id:
        return jsonify(ID_REQUIRED)

    # fetch brewery first
    brewery = query_wrapper(Brewery, id=int(id))[0]

    # fetch beers
    return jsonify(to_json(brewery.beers, beer_fields))