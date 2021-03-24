import json
import os
import uuid
from flask import Flask, render_template, send_from_directory, request, flash,\
    redirect
import numpy as np

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
    analyzer.models_calculation(int(sample))
    sample = analyzer.samples[int(sample)]
    # x = list(np.arange(0, 1.1, 0.1))
    # x = [point.p_p1 for point in sample.points if point.adsorb_or_desorb == 0]
    y_adsorb = [[point.p_p1, point.volume] for point in sample.points if point.adsorb_or_desorb == 0]
    y_desorb = [[point.p_p1, point.volume] for point in sample.points if point.adsorb_or_desorb == 1]

    data = [[
        y_adsorb,
        y_desorb
        # 'x': x,
        # 'y_adsorb': y_adsorb,
        # 'y_desorb': y_desorb
        ]]

    return json.dumps(data)


@app.route('/plot/<filename>')
def send_plot(filename):
    return send_from_directory(conf.GRAPH_FOLDER, filename)
