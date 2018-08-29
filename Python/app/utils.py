from flask import request, jsonify
import six
import flask_sqlalchemy
from models import session

Column = flask_sqlalchemy.sqlalchemy.sql.schema.Column
InstrumentedAttribute = flask_sqlalchemy.sqlalchemy.orm.attributes.InstrumentedAttribute

# allow safe imports
__all__ = ('collect_args', 'to_json', 'json_exception_handler', 'query_wrapper', 'success',
           'list_fields', 'get_row', 'update_object', 'toGeoJson',  'endpoint_query')

def success(msg, **kwargs):
    """ returns a Response() object as JSON

    :param msg: message to send
    :param kwargs: additional key word arguments to add to json response
    :return: Response() object as JSON
    """
    kwargs['message'] = msg
    kwargs['status'] = 'success'
    return jsonify(kwargs)

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
        for k,v in request.files.iteritems():
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
        #print('conditions: {}'.format(conditions))
        return session.query(table).filter(*conditions).all()
    else:
        return session.query(table).all()

def endpoint_query(table, fields, id=None):
    """ wrapper for for query endpoint that can query one feature by id
    or query all features via the query_wrapper

    :param table: Table to query
    :param fields: fields to be returned in query
    :param id: optional resource ID
    :return: Response() object for query result as json
    """
    if id != None:
        item = query_wrapper(table, id=int(id))
        return jsonify(to_json(item, fields))

    # check for args and do query
    args = collect_args()
    results = query_wrapper(table, **args)
    return jsonify(to_json(results, fields))

def to_json(results, fields=None):
    """casts query results to json

    :param results: query results
    :param fields: list of field names to include
    :return:
    """
    if isinstance(results, list):
        if len(results):
            if not fields or not isinstance(fields, (list, tuple)):
                fields = list_fields(results[0])
            return [{f: getattr(r, f) for f in fields} for r in results]
        else:
            return []
    else:
        if not fields or not isinstance(fields, (list, tuple)):
            fields = list_fields(results)
        return {f: getattr(results, f) for f in fields}

# toGeoJson() handler for results
def toGeoJson(d):
    """ return features as GeoJson (use this for brewery query)

    :param d: dict of features to return as GeoJson
    :return: GeoJson structure as dict
    """
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


def get_row(table, d, key):
    val = d.get(key)
    if val:
        return session.query(table).filter_by(**{key: val}).first()
    return None

def update_object(obj, **kwargs):
    for k,v in six.iteritems(kwargs):
        setattr(obj, k, v)
