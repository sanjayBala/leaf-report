import os
from flask import Flask, render_template, flash, request, redirect, send_from_directory
from forms.main_form import UploadForm
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import pandas as pd
from process import generate_report

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = './'

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadForm()
    message = ''
    if request.method == 'POST':
        file = request.files['file']
        if form.validate_on_submit() and file.filename != '':
            file.save(secure_filename(file.filename))
            print('File Saved')
            folder = os.path.join(app.config['UPLOAD_FOLDER'])
            output_filepath = generate_report(request.form.get('leaf_rate'), file.filename)
            print('Report Generated ' +  output_filepath)
            download_url = get_download_url(output_filepath)
            print('download_url ' + str(download_url))
            return download_url
        else:
            message = 'File Required!'
            flash('File required!')
    return render_template('index.html', form=form, message=message)

def get_download_url(filename):
    uploads = os.path.join(app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)