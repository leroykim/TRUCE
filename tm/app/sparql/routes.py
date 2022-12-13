from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import current_user, login_required
from app.sparql.forms import DataForm
from app.sparql import bp

@bp.route('/query', methods=['GET', 'POST'])
def query():
    form = DataForm()
    if form.validate_on_submit():
        flash('SPARQL query has been generated.')
        #print(form.category.data)
    return render_template('sparql/data_form.html', title='SPARQL', form=form)