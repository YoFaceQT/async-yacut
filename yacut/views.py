from . import app, db
from flask import flash, redirect, render_template, url_for

from .constants import FILES_URL, FORBIDEN_URLS
from .forms import URLMapForm, UploadFilesForm
from .models import URLMap
from .yadisk import upload_files_to_disk



@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Функция главной страницы"""
    form = URLMapForm()
    full_url = None

    if not form.validate_on_submit():
        return render_template('index.html', form=form, full_url=full_url)

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
        short = URLMap.generate_unique_short()

    url_map = URLMap(
        original=original_link,
        short=short
    )
    db.session.add(url_map)
    db.session.commit()

    flash('Ссылка успешно создана!')
    full_url = url_for('redirect_to_original', short=short, _external=True)
    return render_template('index.html', form=form, full_url=full_url)


@app.route(FILES_URL, methods=['GET', 'POST'])
async def files_view():
    """Функция страницы загрузки файлов"""
    form = UploadFilesForm()
    uploaded_files = []

    if not form.validate_on_submit():
        return render_template('files.html', form=form)

    if form.files.data:
        disk_results = await upload_files_to_disk(form.files.data)

        for result in disk_results:
            if 'url' in result:
                short = URLMap.generate_unique_short()

                url_map = URLMap(
                    original=result['url'],
                    short=short,
                )
                db.session.add(url_map)

                uploaded_files.append({
                    'filename': result['filename'],
                    'short_link': short,
                    'full_link': url_for(
                        'redirect_to_original',
                        short=short,
                        _external=True
                    )
                })
            else:
                flash(f'Ошибка при загрузке {result["filename"]}')

        if uploaded_files:
            db.session.commit()
            flash(f'Успешно загружено {len(uploaded_files)} файлов')
    else:
        flash('Выберите файлы для загрузки')

    recent_files = URLMap.query.order_by(URLMap.timestamp.desc()).all()

    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
        recent_files=recent_files
    )


@app.route('/<short>', methods=['GET'])
def redirect_to_original(short):
    """Функция переадресации с короткий ссылки на оригинальную"""
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)