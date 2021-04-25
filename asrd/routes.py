from flask import render_template, request, flash, redirect

from asrd.app import app, basic_auth

from asrd.analyzer import Analyzer

import json


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
        analyzer = Analyzer()
        id = analyzer.parse(file)

        return redirect(f'/view/{id}')
    else:
        flash('Allowed file types are srb')
        return redirect('/')


@app.route('/view/<set_id>/')
@basic_auth.required
def view(set_id):
    analyzer = Analyzer()
    samples = analyzer.get_samples(set_id)

    return render_template('index.html',
                           set_id=set_id,
                           samples=samples)


@app.route('/view/<set_id>/<sample_id>/')
@basic_auth.required
def view_with_graph(set_id, sample_id):
    analyzer = Analyzer()
    samples = analyzer.get_samples(set_id)

    return render_template('index.html',
                           graph=True,
                           set_id=set_id,
                           sample_id=int(sample_id),
                           samples=samples)


@app.route('/api/points/<set_id>/<sample_id>')
@basic_auth.required
def api_get_point(set_id, sample_id):
    analyzer = Analyzer()
    # analyzer.parse(set_id)

    options = analyzer.get_options_for_graphs(sample_id)

    return json.dumps(options)
