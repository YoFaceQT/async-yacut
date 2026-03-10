from . import app, db
from flask import flash, redirect, render_template, url_for
from .forms import URLMapForm, UploadFilesForm
from .models import URLMap
from settings import FORBIDEN_URLS
from .utilits import generate_unique_short
from .yadisk import upload_file_to_disk, upload_files_to_disk, get_upload_url


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


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = UploadFilesForm()
    uploaded_files = []

    if form.validate_on_submit():
        if form.files.data:
            disk_results = upload_files_to_disk(form.files.data)

            for result in disk_results:
                if result['success']:
                    short_link = generate_unique_short()

                    url_map = URLMap(
                        original=result['download_link'],
                        short=short_link,
                    )
                    db.session.add(url_map)

                    uploaded_files.append({
                        'filename': result['filename'],
                        'short_link': short_link,
                        'full_link': url_for('redirect_file', short_link=short_link, _external=True)
                    })
                else:
                    flash(f'Ошибка при загрузке {result["filename"]}: {result["error"]}')

            if uploaded_files:
                db.session.commit()
                flash(f' Успешно загружено {len(uploaded_files)} файлов')

        else:
            flash('Выберите файлы для загрузки')
    recent_files = URLMap.query.order_by(URLMap.timestamp.desc()).limit(5).all()

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
        recent_files=recent_files
    )


@app.route('/f/<short_link>')
def redirect_file(short_link):
    url_map = URLMap.query.filter_by(short=short_link).first_or_404()
    return redirect(url_map.original, code=307)