from flask import request, jsonify
import six
import json
import os
import re
import flask_sqlalchemy
from models import session
import csv
import time
import shapefile
import shutil
import datetime
import operator
import fnmatch
from werkzeug.exceptions import HTTPException

Column = flask_sqlalchemy.sqlalchemy.sql.schema.Column
InstrumentedAttribute = flask_sqlalchemy.sqlalchemy.orm.attributes.InstrumentedAttribute

# download folder
download_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

WGS_1984 = """GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]"""


def load_config():
    config_file = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except:
        return {}

def get_timestamp(s=''):
    """

    Args:
        s:

    Returns:

    """
    return '_'.join(filter(None, [s, time.strftime('%Y%m%d%H%M%S')]))

def clean_filename(path):
    """replaces all special characters with underscores

    Required:
        path -- full path to file or folder
    """
    basename, ext = os.path.splitext(os.path.basename(path))
    fn = re.sub('[^A-Za-z0-9]+', '_', basename).replace('__', '_')
    return os.path.join(os.path.dirname(path), fn + ext)

def success(msg, **kwargs):
    """ returns a Response() object as JSON

    :param msg: message to send
    :param kwargs: additional key word arguments to add to json response
    :return: Response() object as JSON
    """
    kwargs['message'] = msg
    kwargs['status'] = 'success'
    return jsonify(kwargs)

def dynamic_error(errName='FlaskRuntimeError', **kwargs):
    defaults = {
        'code': 501,
        'description': 'Runtime Error',
        'message': 'A runtime error has occured'
    }
    atts = {}
    for k,v in six.iteritems(defaults):
        atts[k] = kwargs.get(k) or defaults[k]

    # create HTTPException Subclass Error dynamically with type()
    de = type(errName, (HTTPException,), atts)
    return json_exception_handler(de)


def json_exception_handler(error):
    response = jsonify({
        'status': 'error',
        'details': {
            'code': error.code,
            'name': error.description,
            'message': error.message
        }
    })

    response.status_code = error.code
    return response

def collect_args():
    """ collects arguments from request including query string, form data, raw json, and files

    :return: dict of request arguments
    """
    # check query string first
    data = {}
    for arg in request.values:
        val = request.args.get(arg, None)
        if val is not None:
            data[arg] = val

    # form data
    for k,v in request.form.iteritems():
        data[k] = v

    # check data attribute as fallback
    request_json = request.get_json() or {}
    for k,v in six.iteritems(request_json):
        data[k] = v
        # no application/json mimetype header...
        try:
            req_data = json.loads(request.data) or {}
            for k,v in six.iteritems(req_data):
                data[k] = v
        except:
            pass

    # finally, check for files
    if request.files:
        for k,v in six.iteritems(request.files):
            data[k] = v
    return data

def list_fields(table):
    if not table:
        return []
    cols = table.__table__.columns if hasattr(table, '__table__') else table.columns
    return [f.name for f in cols]


def query_wrapper(table, **kwargs):
    """query wrapper for complex queries via kwargs

    Required:
        table -- db.Model() for table

    Optional:
        **kwargs -- dict/kwargs of conditions for query
        wildcards -- list of field names that should use like query
            instead of equals (string contains)
    """
    conditions = []
    wildcards = kwargs.get('wildcards', [])
    if isinstance(wildcards, six.string_types):
        wildcards = wildcards.split(',')
    for kwarg, val in six.iteritems(kwargs):
        if hasattr(table, kwarg):
            col = getattr(table, kwarg)
            if isinstance(col, (Column, InstrumentedAttribute)):
                if kwarg in wildcards:
                    conditions.append(col.like('%{}%'.format(val)))
                else:
                    conditions.append(col==val)
    if conditions:
        return session.query(table).filter(*conditions).all()
    else:
        return session.query(table).all()

def endpoint_query(table, fields=None, id=None, **kwargs):
    """ wrapper for for query endpoint that can query one feature by id
    or query all features via the query_wrapper

    :param table: Table to query
    :param fields: fields to be returned in query
    :param id: optional resource ID
    :return: Response() object for query result as json
    """
    if id != None:
        item = query_wrapper(table, id=int(id))[0]
        return jsonify(to_json(item, fields))

    # check for args and do query
    args = collect_args()
    print('args: ', args)
    for k,v in six.iteritems(kwargs):
        args[k] = v
    results = query_wrapper(table, **args)
    return jsonify(to_json(results, fields))

def validate_fields(table, fields=None):
    """

    :param table:
    :param fields:
    :return:
    """
    if isinstance(fields, six.string_types):
        fields = map(lambda f: f.strip(), fields.split(','))
    if not fields or not isinstance(fields, (list, tuple)):
        fields = list_fields(table)
    return fields

def to_json(results, fields=None):
    """casts query results to json

    :param results: query results
    :param fields: list of field names to include
    :return:
    """
    fields = validate_fields(results[0] if isinstance(results, list) and len(results) else results, fields)
    if isinstance(results, list):
        if len(results):
            return [{f: getattr(r, f) for f in fields} for r in results]
        else:
            return []
    else:
        return {f: getattr(results, f) for f in fields}

def export_to_shapefile(table, fields=None, **kwargs):
    results = toGeoJson(to_json(query_wrapper(table, **kwargs), fields=fields))
    features = results.get('features')
    if not len(features):
        return None

    # field mapping
    field_map = {
        'id':  { 'type': 'N' },
        'name': { 'type': 'C', 'size': '100' },
        'address': { 'type': 'C', 'size': '100' },
        'city': { 'type': 'C', 'size': '50' },
        'state': { 'type': 'C', 'size': '2' },
        'zip': { 'type': 'C', 'size': '11' },
        'monday': { 'type': 'C', 'size': '30' },
        'tuesday': {'type': 'C', 'size': '30'},
        'wendesday': {'type': 'C', 'size': '30'},
        'thursday': {'type': 'C', 'size': '30'},
        'friday': {'type': 'C', 'size': '30'},
        'saturday': {'type': 'C', 'size': '30'},
        'sunday': {'type': 'C', 'size': '30'},
        'comments': {'type': 'C', 'size': '255'},
        'brew_type': { 'type': 'C', 'size': '50' },
        'website': {'type': 'C', 'size': '255' },
        'x': { 'type': 'F' },
        'y': {'type': 'F'},
    }

    # create output folder for zipping up shapefile
    basename = get_timestamp(table.__tablename__)
    folder = os.path.join(download_folder, basename)
    output = os.path.join(folder, basename)
    if not os.path.exists(folder):
        os.makedirs(folder)

    # build schema based on first record
    first = features[0].get('properties', {})
    field_list = filter(lambda f: f in field_map and f in first, list_fields(table))

    # open shapefile writer
    with shapefile.Writer(output, 1) as w:

        # add fields
        for field in field_list:
            # get field definition
            fd = field_map.get(field, {})

            # specify name, type, field size, decimal size
            w.field(field, fd.get('type'), fd.get('size', '50'), 6 if fd.get('type') == 'F' else 0)

        # add features
        for feature in features:
            # write geometry first (accepts geojson)
            w.shape(feature.get('geometry'))

            # write attributes, filter by queried fields only
            w.record(**{f: feature.get('properties', {}).get(f) for f in field_list })

    # write .prj file with WGS 1984 coordinate info
    prj = os.path.join(folder, basename + '.prj')
    with open(prj, 'w') as f:
        f.write(WGS_1984)

    # zip all files for shapefile
    shutil.make_archive(folder, 'zip', folder)
    try:
        shutil.rmtree(folder)
    except:
        pass
    return folder + '.zip'


def export_data(table, fields=None, format='csv', **kwargs):
    # cleanup download directory by deleting files older than 30 minutes
    remove_files(download_folder, minutes=30)

    # get fields
    fields = validate_fields(table, fields)

    # allow shapefile export if table selected is breweries
    if format.lower() == 'shapefile' and table.__tablename__ == 'breweries':
        return export_to_shapefile(table, fields, **kwargs)

    else:
        # export data as csv
        results = to_json(query_wrapper(table, fields=fields, **kwargs), fields)

        # write csv file
        csvFilePath = os.path.join(download_folder, '{}.csv'.format(get_timestamp(table.__tablename__)))

        with open(csvFilePath, 'wb') as csvFile:
            writer = csv.DictWriter(csvFile, fields)
            writer.writeheader()
            for result in results:
                writer.writerow(result)

        return csvFilePath


# toGeoJson() handler for breweries
def toGeoJson(d):
    """ return features as GeoJson (use this for brewery query)

    :param d: dict of features to return as GeoJson
    :return: GeoJson structure as dict
    """
    if not isinstance(d, list):
        d = [d]
    return {
        "type": "FeatureCollection",
        # "crs": {
        #     "type": "name",
        #     "properties": {
        #         "name": "urn:ogc:def:crs:EPSG::3857"
        #     }
        # },
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

def remove_files(path, exclude=[], older_than=True, test=False, subdirs=False, pattern='*', **kwargs):
    """removes old folders within a certain amount of days from today
    Required:
        path -- root directory to delete files from
        days -- number of days back to delete from.  Anything older than
            this many days will be deleted. Default is 7 days.
    Optional:
        exclude -- list of folders to skip over (supports wildcards).
            These directories will not be removed.
        older_than -- option to remove all folders older than a certain
            amount of days. Default is True.  If False, will remove all
            files within the last N days.
        test -- Default is False.  If True, performs a test folder iteration,
            to print out the mock results and does not actually delete files.
        subdirs -- iterate through all sub-directories. Default is False.
        pattern -- wildcard to match name scheme for files to delete, default is "*"
    """
    # if not kwargs, default to delete things older than one day
    deltas = ['days', 'months', 'years', 'weeks', 'hours', 'minutes', 'seconds']
    time_args = {}
    for k,v in kwargs.iteritems():
        if k in deltas:
            time_args[k] = v
    if not time_args:
        time_args['days'] = 1

    # get removal date and operator
    remove_after = datetime.datetime.now() - datetime.timedelta(**time_args)
    op = operator.lt
    if not older_than:
        op = operator.gt

    # optional test
    if test:
        def remove(*args): pass
    else:
        def remove(*args):
            os.remove(args[0])

    # walk thru directory
    for root, dirs, files in os.walk(path):
        if not root.endswith('.gdb'):
            for f in files:
                if not f.lower().endswith('.lock') and fnmatch.fnmatch(f, pattern):
                    if not any(map(lambda ex: fnmatch.fnmatch(f, ex), exclude)):
                        last_mod = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, f)))

                        # check date
                        if op(last_mod, remove_after):
                            try:
                                remove(os.path.join(root, f))
                                print('deleted: "{0}"'.format(os.path.join(root, f)))
                            except:
                                print('\nCould not delete: "{0}"!\n'.format(os.path.join(root, f)))
                        else:
                            print('skipped: "{0}"'.format(os.path.join(root, f)))
                    else:
                        print('excluded: "{0}"'.format(os.path.join(root, f)))
                else:

                    print('skipped file: "{0}"'.format(os.path.join(root, f)))
        else:
            print('excluded files in: "{0}"'.format(root))

        # break or continue if checking sub-directories
        if not subdirs:
            break

    return


def get_object(table, **kwargs):#, d, key):
    # val = d.get(key)
    # if val:
    try:
        return session.query(table).filter_by(**kwargs).first()
    except:
        return None

def create_object(table, **kwargs):
    return table(**kwargs)

def update_object(obj, **kwargs):
    for k,v in six.iteritems(kwargs):
        setattr(obj, k, v)
    return obj

def delete_object(obj):
    oid = obj.id
    obj.delete() if hasattr(obj, 'delete') else session.delete(obj)
    return oid

