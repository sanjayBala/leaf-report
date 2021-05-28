import os
from flask import Flask, render_template, flash, request, redirect, send_from_directory

from werkzeug.utils import secure_filename
import pandas as pd

from process import generate_report

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = './'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded, try again!')
            return render_template('index.html')
        else:
            file = request.files['file']
            file.save(secure_filename(file.filename))
            output_filepath = generate_report(request.form.get('leaf_rate'), file.filename)
            return download(output_filepath)
    return render_template('index.html')


@app.route('/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)