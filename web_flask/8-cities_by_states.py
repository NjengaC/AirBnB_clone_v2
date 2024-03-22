#!/usr/bin/python3
"""
This is Module Documentation- starts a Flask web application

"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays page with a list of all State objects and their cities"""

    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    states_wth_cities = []
    for state in sorted_states:
        cities = storage.all(City).values()
        state_dict = state.to_dict()
        ctys = [city.to_dict() for city in cities if city.state_id == state.id]
        sorted_cities = sorted(ctys, key=lambda city: city['name'])
        state_dict['cities'] = sorted_cities
        states_wth_cities.append(state_dict)

    return render_template("8-cities_by_states.html", states=states_wth_cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
