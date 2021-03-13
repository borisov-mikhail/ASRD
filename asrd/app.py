import os
from flask import Flask, render_template, send_from_directory, request, flash,\
    redirect, url_for
from werkzeug.utils import secure_filename
from asrd.analyzer import Analyzer

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'srb'}
app.secret_key = "secret key"

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/plot/<name>')
def send_plot(name):
    return send_from_directory('../data', name)


def allowed_file(filename):
    if '/' in filename:
        return False

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload-srb-data/', methods=['POST'])
def upload_srb_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')

    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect('/')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        filename_without_ext = filename.replace('.srb', '')
        return redirect(f'/view/{filename_without_ext}')
    else:
        flash('Allowed file types are srb')
        return redirect(request.url)


@app.route('/view/<file>/')
def view(file):
    analyzer = Analyzer()
    analyzer.parse(os.path.join(app.config['UPLOAD_FOLDER'], f'{file}.srb'))
    samples_names = analyzer.get_samples_names()

    return render_template('index.html', file=file, samples=enumerate(samples_names))


@app.route('/view/<file>/<sample_index>/')
def view_with_graph(file, sample_index):
    analyzer = Analyzer()
    analyzer.parse(os.path.join(app.config['UPLOAD_FOLDER'], f'{file}.srb'))
    samples_names = analyzer.get_samples_names()

    return render_template('index.html', graph='test', samples=enumerate(samples_names))
