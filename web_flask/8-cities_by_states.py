#!/usr/bin/python3


"""Initiates a Flask web app
   Listens to 0.0.0.0 on port 5000
"""
from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def list_cities_by_states():
    """Display a list of states and their cities, sorted by name."""
    states = storage.all(State).values()
    for state in states:
        state.cities = sorted(state.cities, key=lambda city: city.name)
    states = sorted(states, key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown():
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
