#!/usr/bin/python3
# from tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
from flask_app import app

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port = 5050)