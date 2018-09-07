from base import FlaskExtension
from flask import jsonify
import os
import zipfile
from brewery_api import brewery_api
from security import security_api, userStore, unauthorized_callback
from flask_login import LoginManager, login_required
import shapefile
import shutil
import glob
from utils import *
from models import session
from datetime import timedelta
from exceptions import UserNotFound

# downloads folder for exports
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# init app inherited from our base.FlaskExtension object
app_name = os.path.basename(__file__).split('.')[0]
app = FlaskExtension(app_name, static_url_path=download_folder)

# set secret key and cookie name for flask-login
app.config['SECRET_KEY'] = 'beer-app'
app.config['REMEMBER_COOKIE_NAME'] = 'beer_app_token'

# register flask-login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.unauthorized_handler(unauthorized_callback)

# register blueprints to get functionality from brewery and security api's
app.register_blueprint(brewery_api)
app.register_blueprint(security_api)

# callback to reload the user object for flask-login
@login_manager.user_loader
def load_user(userid):
    print('USERID IS: ', userid)
    # with open('./text.txt', 'w') as f:
    #     f.write(userid)
    return userStore.get_user(id=userid)

@login_manager.request_loader
def load_user_from_request(request):
    """allow users to be loaded via request params or authorization header"""
    # check for token in request params or in Authorization header
    args = collect_args()
    print('args from request_loader: ', args)
    token = args.get('token') or request.headers.get('Authorization')
    if token:
        try:
            return userStore.get_user(token=token)
        except UserNotFound:
            return None

    return None


# API METHODS BELOW
@app.route('/')
def hello():
    return jsonify({'message': 'welcome to the brewery api!'})

@app.route('/test')
def test():
    return jsonify(collect_args())

@app.route('/conversion/toGeoJson', methods=['POST'])
@login_required
def toGeoJson():
    # get arguments
    args = collect_args()
    zipped = args.get('zipped')

    if not zipped:
        return app.json_error(error='No Zip file uploaded!')

    # write zipped file to temp dir
    scratch = os.path.join(os.environ['TEMP'], 'scratch')
    if not os.path.exists(scratch):
        os.makedirs(scratch)
    fold = os.path.join(scratch, 'upload_{}'.format(app.get_timestamp()))
    with open(fold + '.zip', 'wb') as f:
        f.write(zipped.read())

    # unzip zipped file
    with zipfile.ZipFile(fold + '.zip', 'r') as f:
        f.extractall(fold)

    print('extracted to: "{}"'.format(fold))
    # get fc and conver to json
    # having issues with arcpy saying shapefile doesn't exist, even though FeaturesToJSON works???
    shp = glob.glob(os.path.join(fold, '*.shp'))[0]

    # convert to geojson
    reader = shapefile.Reader(shp)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    features = []
    for sr in reader.shapeRecords():
        attr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        features.append({
            'type': 'Feature',
            'geometry': geom,
            'properties':attr
        })

    # cleanup temp files
    try:
        os.remove(fold + '.zip')
        shutil.rmtree(fold)
    except:
        print 'cleanup failed'

    return jsonify({
        'type': 'FeatureCollection',
        'features': features
    })
