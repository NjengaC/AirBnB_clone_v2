#!/usr/bin/python3
"""
This is a script that starts a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display a list of all State objects in the database.
    """
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda s: s.name)
    return render_template('states_list.html', states=states_sorted)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Remove the current SQLAlchemy Session after each request.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
