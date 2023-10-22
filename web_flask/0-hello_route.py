#!/usr/bin/python3

"""Initiates a Flask web app
   Listens to 0.0.0.0 on 5000
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Displays Hello HBNB!"""
    return 'Hello HBNB!'


# @app.route("/hbnb", strict_slashes=False)
# def hello():
#    """Displays HBNB"""
#    return 'HBNB'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
