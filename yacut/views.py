from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import UrlForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    short_url = None
    if form.validate_on_submit():
        if not form.custom_id.data:
            short_url = get_unique_short_id()
        else:
            short_url = form.custom_id.data
        exist = URLMap.query.filter_by(
            original=form.original_link.data
        ).first()
        if exist:
            flash('Предложенный вариант короткой ссылки уже существует.')
        else:
            new_url = URLMap(
                original=form.original_link.data,
                short=short_url
            )
            db.session.add(new_url)
            db.session.commit()
            flash(url_for(
                "redirect_to_original",
                short_id=short_url,
                _external=True
            )
            )
    return render_template('form.html', form=form)


@app.route('/<short_id>')
def redirect_to_original(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url:
        return redirect(url.original)
    else:
        abort(404)
