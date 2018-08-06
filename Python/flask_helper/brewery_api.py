from flask import jsonify, Blueprint, request, send_file
from models import *
from sqlalchemy.orm import sessionmaker
from utils import *
from io import BytesIO

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
BeerPhotos.query = session.query(BeerPhotos)

# get list of brewery fields to use as default
brewery_fields = list_fields(Brewery)
beer_fields = list_fields(Beer)
beer_photo_fields = filter(lambda f: f != 'data', list_fields(BeerPhotos))


# constants
PHOTO_MIMETYPE = 'application/octet-stream'
ID_REQUIRED = {'error': {'code': 404, 'message': 'an ID is required'}}
INVALID_ID = {'error': {'code': 404, 'message': 'an Invalid ID was supplied'}}


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
    return jsonify(handler(to_json(results, fields)))

@brewery_api.route('/breweries/<id>/beers')
def get_beers_from_brewery(id=None):
    if not id:
        return jsonify(ID_REQUIRED)

    # fetch brewery first
    brewery = query_wrapper(Brewery, id=int(id))[0]

    # fetch beers
    return jsonify(to_json(brewery.beers, beer_fields))

@brewery_api.route('/beers')
@brewery_api.route('/beers/<id>')
def get_beer_by_id(id=None):
    if id:
        beer = query_wrapper(Beer, id=int(id))
        return jsonify(to_json(beer, beer_fields))

    # check for args and do query
    args = collect_args()
    results = query_wrapper(Beer, **args)
    return jsonify(to_json(results, beer_fields))


@brewery_api.route('/beers/<id>/photos')
def get_beer_photos(id=None):
    if not id:
        return jsonify(ID_REQUIRED)

    beer = query_wrapper(Beer, id=int(id))[0]
    return jsonify(to_json(beer.photos, beer_photo_fields))

@brewery_api.route('/beer_photos')
@brewery_api.route('/beer_photos/<id>')
def get_beer_photo(id=None):
    if id:
        beer_photo = query_wrapper(BeerPhotos, id=int(id))[0]
        return jsonify(to_json(beer_photo, beer_photo_fields))

    # check for args and do query
    args = collect_args()
    results = query_wrapper(BeerPhotos, **args)
    return jsonify(to_json(results, beer_photo_fields))

@brewery_api.route('/beer_photos/<id>/download')
def download_beer_photo(id):
    if not id:
        return jsonify(ID_REQUIRED)

    beer_photo = query_wrapper(BeerPhotos, id=int(id))[0]
    return send_file(BytesIO(beer_photo.data), attachment_filename=beer_photo.photo_name, as_attachment=True)
