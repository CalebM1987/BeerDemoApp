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
from security import security_api, Users, userStore
from flask_login import LoginManager

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(brewery_api)
app.register_blueprint(security_api)

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return userStore.get_user(id=userid)

if __name__ == '__main__':
    #host= '169.254.99.131'
    app.run(debug=True)
