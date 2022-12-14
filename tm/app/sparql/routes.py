from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import current_user, login_required
from app.sparql.forms import DataForm, SPARQLForm
from app.sparql import bp

@bp.route('/query', methods=['GET', 'POST'])
def query():
    form = DataForm()
    if form.validate_on_submit():
        flash('SPARQL query has been generated.')
        selection = \
            f"Category={form.category.data}\
                Name={form.name.data}\
                    Age={form.age.data}"
    else:
        selection=None
    return render_template('sparql/data.html', title='DATA', 
                            form=form, selection=selection)

@bp.route('/query_raw', methods=['GET', 'POST'])
def query_raw():
    form = SPARQLForm()
    if form.validate_on_submit():
        flash('SPARQL query has been generated.')
        result = f"{form.sparql_query.data}"
    else:
        result=None
    return render_template('sparql/sparql.html', title='SPARQL', 
                            form=form, result=result)