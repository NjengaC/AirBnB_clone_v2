from flask import Flask, render_template

app = Flask(__name__)


# Route to display "Hello HBNB!"
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'


# Route to display "HBNB"
@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


# Route to display "“C ” followed by the value of the text variable"
@app.route('/c/<text>', strict_slashes=False)
def C_is_fun(text):
    text = text.replace('_', ' ')
    return 'C ' + text


# Route to display "“Python ” followed by the value of the text variable"
# Default text is cool
@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def python_route(text="is cool"):
    text = text.replace('_', ' ')
    return 'Python ' + text


# Route to display "“n is a number" ONLY if n is an integer"
@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    return  "{} is a number".format(n)


# Route to display a HTML page ONLY if n is an integer"
@app.route('/number_template/<int:n>', strict_slashes=False)
def number_temp(n):
    return render_template("5-number.html", n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
