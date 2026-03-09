import random
import string

from . import app, db
from flask import flash, redirect, render_template, url_for
from .forms import URLMapForm, UploadFilesForm
from .models import URLMap

FORBIDEN_URLS = ['files']


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    created_short = None

    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id:
            if (URLMap.query.filter_by(short=custom_id).first() is not None
                    or custom_id in FORBIDEN_URLS):
                flash('Предложенный вариант короткой ссылки уже существует.', 'danger')
                return render_template('index.html', form=form, created_short=created_short)

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
        created_short = short
        return render_template(
            'index.html', form=form, created_short=created_short
        )

    return render_template(
        'index.html', form=form, created_short=created_short
    )


def generate_unique_short(length=6):
    """Генерирует уникальную короткую ссылку"""
    while True:
        short = ''.join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )

        if (URLMap.query.filter_by(short=short).first() is None
                and short not in FORBIDEN_URLS):
            return short


@app.route('/<short>')
def redirect_to_original(short):
    """Редирект с короткой ссылки на оригинальную"""
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)


@app.route('/files')
def files_view():
    form = UploadFilesForm()
    return render_template('files.html', form=form)