#!/usr/bin/python3


"""Initiates a Flask web app
   Listens to 0.0.0.0 on port 5000
"""
from flask import Flask, render_template
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


@app.route("/number/<int:n>", strict_slashes=False)
def check_number(n):
    """Displays 'n is a number' only if n is an integer."""
    return f"{escape(n)} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def display_number_template(n):
    """Displays an HTML page only if <n> is an integer."""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def display_int_odd_or_even(n):
    """State whether <n> is odd or even."""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
