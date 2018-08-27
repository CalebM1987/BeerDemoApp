#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     08/27/2018
# Copyright:   (c) calebma 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from base import FlaskExtension
from flask import jsonify, request
import json
import os
import zipfile
import sys
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'lib'))
from brewery_api import brewery_api
from security import security_api, userStore
from flask_login import LoginManager
import shapefile

# init app
app_name = os.path.basename(__file__).split('.')[0]
app = FlaskExtension(app_name)
app.config['SECRET_KEY'] = 'beer-app'
app.config['REMEMBER_COOKIE_NAME'] = 'beer_app_token'

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# register blueprints to get functionality from brewery and security api's
app.register_blueprint(brewery_api)
app.register_blueprint(security_api)

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return userStore.get_user(id=userid)

# API METHODS BELOW
@app.route('/')
def hello():
    return jsonify({'message': 'wellcome to the brewery api!'})

@app.route('/test')
def test():
    return jsonify(collect_args())

@app.route('/conversion/toGeoJson', methods=['POST'])
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

    print 'extracted to: "{}"'.format(fold)
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


if __name__ == '__main__':

    # run app on default port 5000
    app.run(debug=True, port=5000)
