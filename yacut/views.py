import asyncio

from flask import redirect, render_template, request, url_for

from . import app, db
from .forms import URLMapForm, FilesForm
from .models import URLMap
from .utils import get_unique_short_id
from .constants import DUPLICATE_MESSAGE
from .disk import upload_to_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    message = None
    short_link = None

    if form.validate_on_submit():
        short_id = form.custom_id.data

        if short_id:
            if (
                short_id == 'files'
                or URLMap.query.filter_by(short=short_id).first() is not None
            ):
                message = DUPLICATE_MESSAGE
        else:
            short_id = get_unique_short_id()

        if message is None:
            url_map = URLMap(
                original=form.original_link.data,
                short=short_id
            )
            db.session.add(url_map)
            db.session.commit()

            short_link = url_for(
                'redirect_view',
                short_id=short_id,
                _external=True
            )

    return render_template(
        'index.html',
        form=form,
        short_link=short_link,
        message=message
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
def files_view():
    form = FilesForm()

    uploaded = []

    if form.validate_on_submit():

        files = request.files.getlist('files')

        for file in files:

            download_link = asyncio.run(
                upload_to_disk(file)
            )

            short = get_unique_short_id()

            url_map = URLMap(
                original=download_link,
                short=short
            )

            db.session.add(url_map)

            uploaded.append({
                'name': file.filename,
                'short_link': url_for(
                    'redirect_view',
                    short_id=short,
                    _external=True
                )
            })

        db.session.commit()

    return render_template(
        'files.html',
        form=form,
        uploaded=uploaded
    )