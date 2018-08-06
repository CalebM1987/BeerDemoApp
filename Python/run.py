import os
import sys
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'flask_helper'))
remove = None
for i,p in enumerate(sys.path):
    if 'bmi_library' in p.lower():
        remove = p
        break
if remove:
    sys.path.remove(p)
from app import app
from brewery_api import brewery_api

app.register_blueprint(brewery_api)

if __name__ == '__main__':
    app.run()
