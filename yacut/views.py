from flask import redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm, FilesForm
from .models import URLMap
from .short_id import get_unique_short_id
from .constants import DUPLICATE_MESSAGE
from .disk import upload_to_disk


@app.route('/', methods=('GET', 'POST'))
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
            URLMap.create(
                original=form.original_link.data,
                short=short_id
            )
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


@app.route('/files', methods=('GET', 'POST'))
async def files_view():
    form = FilesForm()

    uploaded = []

    if form.validate_on_submit():

        files = form.files.data

        for file in files:

            download_link = await upload_to_disk(file)

            short_id = get_unique_short_id()

            URLMap.create(
                original=download_link,
                short=short_id
            )

            uploaded.append({
                'name': file.filename,
                'short_link': url_for(
                    'redirect_view',
                    short_id=short_id,
                    _external=True
                )
            })

        db.session.commit()

    return render_template(
        'files.html',
        form=form,
        uploaded=uploaded
    )