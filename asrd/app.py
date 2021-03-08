from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', graph='test')


@app.route('/plot/<name>')
def send_plot(name):
    return send_from_directory('../data', name)

