#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     02/10/2017
# Copyright:   (c) calebma 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from flask_helper import *
import json
import os
import zipfile
import sys
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'flask_helper', 'lib'))
import shapefile
with open(os.path.join(thisDir, 'app_config.json'), 'r') as f:
    config = json.load(f)

# init app
app_name = os.path.basename(__file__).split('.')[0]
app = FlaskExtension(app_name, use_security=True, ldap_server=config.get('ldap_server'), domain_name=config.get('domain_name'))

@app.route('/')
def hello():
    return jsonify({'message': 'hello world!'})

@app.route('/test')
def test():
    return jsonify(collect_args())

# test a secured endpoint, a token must be generated first from inherited "genToken"
#   method of FlaskExtension
@app.route('/security')
@app.authenticate() # must call because of extra arguments, can add "specfic_users" array here to limit who has access
def security():
    return jsonify({'message': 'congratuatlions, you passed security!'})

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
    app.run(debug=True)
