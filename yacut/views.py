from . import app, db
from flask import flash, redirect, render_template

from .constants import FILES_URL
from .forms import UploadFilesForm, URLMapForm
from .models import ShortLinkCreationError, URLMap
from .yadisk import upload_files_to_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Создает короткую ссылку через веб-форму."""
    form = URLMapForm()
    short_link = None

    if not form.validate_on_submit():
        return render_template('index.html', form=form, short_link=short_link)

    try:
        url_map = URLMap.create(
            original=form.original_link.data,
            custom_id=form.custom_id.data
        )

        url_data = url_map.to_dict()
        short_link = url_data['short_link']
        flash('Ссылка успешно создана!')

    except ShortLinkCreationError as e:
        flash(str(e))
        return render_template('index.html', form=form, short_link=short_link)

    return render_template('index.html', form=form, short_link=short_link)


@app.route(f'/{FILES_URL}', methods=['GET', 'POST'])
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
                url_map = URLMap(
                    original=result['url'],
                    short=URLMap.generate_unique_short(),
                )
                db.session.add(url_map)

                file_data = url_map.to_dict()
                file_data['filename'] = result['filename']
                uploaded_files.append(file_data)
            else:
                flash(f'Ошибка при загрузке {result["filename"]}')

        if uploaded_files:
            db.session.commit()
            flash(f'Успешно загружено {len(uploaded_files)} файлов')
    else:
        flash('Выберите файлы для загрузки')

    recent_files = [url_map.to_dict() for url_map in
                    URLMap.query.order_by(URLMap.timestamp.desc()).all()]

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
