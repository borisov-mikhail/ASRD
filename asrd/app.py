import os
from flask import Flask, render_template, send_from_directory, request, flash,\
    redirect, url_for
from werkzeug.utils import secure_filename
from asrd.analyzer import Analyzer

app = Flask(__name__)
analyzer = Analyzer()

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
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            analyzer.parse(filepath)
            samples_names = analyzer.get_samples_names()
            file.save(os.path.join(filepath))
            return render_template('index.html',
                                   graph='test',
                                   samples_names=samples_names)
        else:
            flash('Allowed file types are srb')
            return redirect(request.url)
