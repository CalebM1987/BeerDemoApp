import os
import sys
thisDir = os.path.dirname(__file__)
sys.path.append(os.path.join(thisDir, 'flask_helper'))
from app import app

if __name__ == '__main__':
    app.run()
