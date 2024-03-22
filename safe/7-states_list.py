#!/usr/bin/python3
"""
This is 7-states_list.py Module Documentation

"""
from flask import Flask, render_template
from models import storage
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display a list of all State objects"""
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda s: s.name)
    return render_template('7-states_list.html', states=states_sorted)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
