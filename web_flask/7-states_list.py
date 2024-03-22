#!/usr/bin/python3
"""
This is 7-states_list.py Module Documentation

"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


# Route to display a HTML page ONLY if n is an integer"
@app.route('/states_list', strict_slashes=False)
def list_states():
    """
    This is list_states Function Documentation
    """
    states = storage.all('State').values()
    states_list_dicts = [state.to_dict() for state in states]
    sorted_states = sorted(states_list_dicts, key=lambda state: state['name'])
    return render_template("7-states_list.html", states=sorted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
