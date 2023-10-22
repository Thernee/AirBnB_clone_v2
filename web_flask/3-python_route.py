#!/usr/bin/python3


"""Initiates a Flask web app
   Listens to 0.0.0.0 on port 5000
"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_root():
    """Displays Hello HBNB!"""
    return 'Hello HBNB!'


@app.route("/hbnb", strict_slashes=False)
def hello_hbnb():
    """Displays  HBNB"""
    return 'HBNB'


@app.route("/c/<text>", strict_slashes=False)
def display_text(text):
    """Displays 'C' followed by the value passed as <text>."""
    text = text.replace("_", " ")
    return f"C {escape(text)}"


@app.route("/python/", defaults={'text': "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def display_python_text(text):
    """Displays 'Python' followed by the value passed as <text>."""
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
