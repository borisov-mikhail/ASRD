import json
import os
import uuid
from flask import Flask, render_template, send_from_directory, request, flash,\
    redirect

import asrd.config as conf
from asrd.analyzer import Analyzer

app = Flask(__name__)
app.secret_key = conf.SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload-srb-data/', methods=['POST'])
def upload_srb_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')

    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect('/')

    if file:
        filename = str(uuid.uuid4())
        file.save(os.path.join(conf.UPLOAD_PATH, filename))

        return redirect(f'/view/{filename}')
    else:
        flash('Allowed file types are srb')
        return redirect('/')


@app.route('/view/<guid>/')
def view(guid):
    analyzer = Analyzer()
    analyzer.parse(os.path.join(conf.UPLOAD_PATH, guid))
    samples_names = analyzer.get_samples_names()

    return render_template('index.html',
                           file=guid,
                           samples=enumerate(samples_names))


@app.route('/view/<guid>/<sample_index>/')
def view_with_graph(guid, sample_index):
    analyzer = Analyzer()
    analyzer.parse(os.path.join(conf.UPLOAD_PATH, guid))
    samples_names = analyzer.get_samples_names()
    return render_template('index.html',
                           file=guid,
                           graph=True,
                           sample_index=int(sample_index),
                           samples=enumerate(samples_names))


@app.route('/api/points/<guid>/<sample>')
def api_get_point(guid, sample):
    analyzer = Analyzer()
    analyzer.parse(os.path.join(conf.UPLOAD_PATH, guid))

    options = analyzer.get_options_for_graphs(sample)

    return json.dumps(options)  # data


@app.route('/plot/<filename>')
def send_plot(filename):
    return send_from_directory(conf.GRAPH_FOLDER, filename)
