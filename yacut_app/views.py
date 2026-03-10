from . import app, db
from flask import flash, redirect, render_template, url_for
from .forms import URLMapForm, UploadFilesForm
from .models import URLMap
from settings import FORBIDEN_URLS
from .utilits import generate_unique_short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    full_url = None

    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id:
            if (URLMap.query.filter_by(short=custom_id).first() is not None
                    or custom_id in FORBIDEN_URLS):
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template(
                    'index.html',
                    form=form,
                    full_url=full_url
                )

            short = custom_id
        else:
            short = generate_unique_short()

        url_map = URLMap(
            original=original_link,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()

        flash('Ссылка успешно создана!', 'success')
        full_url = url_for('redirect_to_original', short=short, _external=True)
        return render_template('index.html', form=form, full_url=full_url)

    return render_template('index.html', form=form, full_url=full_url)


@app.route('/<short>')
def redirect_to_original(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)


@app.route('/files')
def files_view():
    form = UploadFilesForm()
    return render_template('files.html', form=form)