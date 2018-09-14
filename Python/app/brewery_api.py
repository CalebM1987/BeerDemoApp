from flask import url_for, Blueprint, send_file
from models import *
from exceptions import *
import utils
reload(utils)
from utils import *
from io import BytesIO

# add brewery API blueprint
brewery_api = Blueprint('brewery_api', __name__)

# get list of brewery fields to use as default
brewery_fields = list_fields(Brewery)
beer_fields = list_fields(Beer)
beer_photo_fields = filter(lambda f: f not in ('data', 'thumbnail'), list_fields(BeerPhotos))

# constants
PHOTO_MIMETYPE = 'application/octet-stream'
category_fields = list_fields(Category)
style_fields = list_fields(Style)
table_dict = {
    'breweries': Brewery,
    'beers': Beer,
    'styles': Style,
    'categories': Category
}


# REST API METHODS BELOW

@brewery_api.route('/beer/categories')
@brewery_api.route('/beer/categories/<id>')
def get_categories(id=None):
    return endpoint_query(Category, category_fields, id)

@brewery_api.route('/beer/categories/<id>/styles')
def get_category_styles(id):
    if id:
        category_styles = query_wrapper(Category, id=int(id))[0].styles
        return jsonify(to_json(category_styles, style_fields))

@brewery_api.route('/beer/styles')
@brewery_api.route('/beer/styles/<id>')
def get_styles(id=None):
    return endpoint_query(Style, style_fields, id)
    # if id:
    #     style = query_wrapper(Style, id=int(id))[0]
    #     js = to_json(style, style_fields)
    #
    #     # append category from relationship
    #     js['category'] = style.category.cat_name
    #     return jsonify(js)
    #
    # # check for args and do query
    # args = collect_args()
    # results = query_wrapper(Style, **args)
    # js = []
    # for r in results:
    #     d = to_json(r, style_fields)
    #
    #     # append category from relationship
    #     d['category'] = r.category.cat_name
    #     js.append(d)
    # return jsonify(js)


@brewery_api.route('/breweries')
@brewery_api.route('/breweries/<id>')
def get_breweries(id=None):
    args = collect_args()
    f = args.get('f', 'json')
    handler = toGeoJson if f.lower() == 'geojson' else lambda t: t
    fields = args.get('fields') or brewery_fields

    if id:
        brewery = query_wrapper(Brewery, id=int(id))[0]
        return jsonify(handler(to_json(brewery, fields)))

    # query as normal
    results = query_wrapper(Brewery, **args)
    return jsonify(handler(to_json(results, fields)))

@brewery_api.route('/breweries/<id>/beers')
@brewery_api.route('/breweries/<id>/beers/<bid>')
def get_beers_from_brewery(id=None, bid=None):
    if not id:
        raise InvalidResource

    # fetch brewery first
    brewery = query_wrapper(Brewery, id=int(id))[0]

    # fetch beers
    if bid:
        try:
            beers = brewery.beers
            # should be a way to achieve this via filter or join?
            return jsonify(to_json([b for b in beers if b.id ==int(bid)][0], beer_fields))
        except Exception as e:
            #return jsonify({'error': str(e), })
            raise InvalidResource
    return jsonify(to_json(brewery.beers, beer_fields))

@brewery_api.route('/beers')
@brewery_api.route('/beers/<id>')
def get_beer_by_id(id=None):
    return endpoint_query(Beer, id=id)

@brewery_api.route('/beers/<id>/photos')
def get_beer_photos(id=None):
    if not id:
        raise InvalidResource

    beer = query_wrapper(Beer, id=int(id))[0]
    return jsonify(to_json(beer.photos, beer_photo_fields))

@brewery_api.route('/beer_photos')
@brewery_api.route('/beer_photos/<id>')
def get_beer_photo(id=None):
    return endpoint_query(BeerPhotos, beer_photo_fields, id)

@brewery_api.route('/beer_photos/<id>/download')
def download_beer_photo(id):
    if not id:
        raise InvalidResource

    beer_photo = query_wrapper(BeerPhotos, id=int(id))[0]
    return send_file(BytesIO(beer_photo.data), attachment_filename=beer_photo.photo_name, as_attachment=True)

@brewery_api.route('/data/<tablename>/export', methods=['POST'])
def export_table_data(tablename):
    table = table_dict.get(tablename)
    print(tablename, table)
    if table:
        args = collect_args()
        fields = args.get('fields')
        f = args.get('f', 'csv')
        if fields:
            del args['fields']
        csvFile = export_data(table, fields, f, **args)
        url = url_for('static', filename=os.path.basename(csvFile))
        return success('Successfully exported data', url=url)
    raise InvalidResource