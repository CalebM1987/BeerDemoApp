import os
import sys
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'flask_helper'))
from app import app
from brewery_api import brewery_api

app.register_blueprint(brewery_api)

if __name__ == '__main__':
    app.run()
