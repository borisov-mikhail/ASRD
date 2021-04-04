import json
import os
import uuid

from flask import render_template, request, flash, redirect

import asrd.config as conf
from asrd import app, basic_auth
from asrd.analyzer import Analyzer


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


@app.route('/upload-srb-data/', methods=['POST'])
@basic_auth.required
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
@basic_auth.required
def view(guid):
    analyzer = Analyzer()
    analyzer.parse(guid)
    samples_names = analyzer.get_samples_names(guid)

    return render_template('index.html',
                           file=guid,
                           samples=enumerate(samples_names))


@app.route('/view/<guid>/<sample_index>/')
@basic_auth.required
def view_with_graph(guid, sample_index):
    analyzer = Analyzer()
    analyzer.parse(guid)
    samples_names = analyzer.get_samples_names(guid)
    return render_template('index.html',
                           file=guid,
                           graph=True,
                           sample_index=int(sample_index),
                           samples=enumerate(samples_names))


@app.route('/api/points/<guid>/<sample>')
@basic_auth.required
def api_get_point(guid, sample):
    analyzer = Analyzer()
    analyzer.parse(guid)

    options = analyzer.get_options_for_graphs(sample)

    return json.dumps(options)
