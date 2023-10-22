#!/usr/bin/python3

"""Initiates a Flask web app
   Listens to 0.0.0.0 on 5000
"""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    """Displays Hello HBNB!"""
    return 'Hello HBNB!'


if __name__ == "__main__":
    app.run(host=0.0.0.0)
