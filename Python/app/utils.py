import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from werkzeug.exceptions import default_exceptions, HTTPException, Unauthorized
from flask import Flask, request, jsonify, current_app, Response, make_response
import ldap
import six
import flask_sqlalchemy

Column = flask_sqlalchemy.sqlalchemy.sql.schema.Column
InstrumentedAttribute = flask_sqlalchemy.sqlalchemy.orm.attributes.InstrumentedAttribute

VALID_CREDENTIALS = 'VALID_CREDENTIALS'
INVALID_CREDENTIALS = 'INVALID_CREDENTIALS'

# allow safe imports
__all__ = ('collect_args', 'SecurityHandler', 'JSONExceptionHandler', 'INVALID_CREDENTIALS',
           'VALID_CREDENTIALS', 'query_wrapper', 'to_json',
           'list_fields', 'get_row', 'update_row', 'toGeoJson')

def collect_args():
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
        return table.query.filter(*conditions).all()
    else:
        return table.query.all()

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
        return table.query.filter_by(**{key: val}).first()
    return None

def update_row(table, **kwargs):
    for k,v in six.iteritems(kwargs):
        setattr(table, k, v)

class SecurityHandler(object):
    def __init__(self, ldap_server, domain_name):
        self._ldap_server = ldap_server
        self.domain_name = domain_name

    def validate_AD(self, usr, pw='xxx'):
        usr = usr.split('\\')[-1]
        dn = '{}\\{}'.format(self.domain_name, usr.split('\\')[-1])  #username with domain validation
        print 'pw is: ', pw
        try:
            conn = ldap.initialize(self._ldap_server)
            conn.protocol_version = 3
            conn.set_option(ldap.OPT_REFERRALS, 0)
            conn.simple_bind_s(dn, pw or 'xxx')  # need to be able to throw an error off an invalid pw
            return VALID_CREDENTIALS
        except ldap.INVALID_CREDENTIALS:
            return INVALID_CREDENTIALS

class JSONExceptionHandler(object):
    """https://coderwall.com/p/xq88zg/json-exception-handler-for-flask"""

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def std_handler(self, error):
        response = jsonify(message=error.message)
        response.status_code = error.code if isinstance(error, HTTPException) else 500
        return response

    def init_app(self, app):
        self.app = app
        self.register(HTTPException)
        for code, v in default_exceptions.iteritems():
            self.register(code)

    def register(self, exception_or_code, handler=None):
        self.app.errorhandler(exception_or_code)(handler or self.std_handler)
