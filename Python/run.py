from app import app

if __name__ == '__main__':

    # run the app, this MUST be wrapped in main thread, we will be running the dev server on port 5000
    host = 'dev.localhost.com'
    host = '192.168.1.20'
    host='0.0.0.0'
    app.run(debug=True, port=5000)#, host=host)