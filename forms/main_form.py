from flask import url_for, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    file = FileField('File')
    leaf_rate = FloatField('Leaf Rate', validators=[DataRequired()])
    submit = SubmitField('Continue!')