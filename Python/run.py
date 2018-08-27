import sys

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
# for my own personal library only, please ignore :)
remove = None
for i,p in enumerate(sys.path):
    if 'bmi_library' in p.lower():
        remove = p
        break
if remove:
    sys.path.remove(p)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

# import app module
from app import app

if __name__ == '__main__':

    # run the app, this MUST be wrapped in main thread
    app.run(debug=True, port=5000)
