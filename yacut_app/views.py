from . import app, db
from flask import render_template
from .forms import URLMapForm, UploadFilesForm


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    return render_template('index.html', form=form)


@app.route('/files')
def files_view():
    form = UploadFilesForm()
    return render_template('files.html', form=form)