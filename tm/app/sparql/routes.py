from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import current_user, login_required
from app.sparql.forms import SPARQLForm, PatientDataForm
from app.sparql import bp
from .fuseki import send_query
from .query import get_patient_select_clause, get_where_clause


@bp.route('/data', methods=['GET', 'POST'])
def query_patient():
    form = PatientDataForm()
    if form.validate_on_submit():
        flash('SPARQL query has been generated.')
        selection = get_patient_select_clause(form)
        where_clause = get_where_clause(form)
        complete_query = selection + where_clause
    else:
        complete_query = None
    return render_template('sparql/patient.html', title='PATIENT DATA',
                           form=form, result=complete_query)


@bp.route('/sparql', methods=['GET', 'POST'])
def query_sparql():
    form = SPARQLForm()
    if form.validate_on_submit():
        flash('SPARQL query has been sent.')
        result = send_query(form.sparql_query.data)
    else:
        result = None
    return render_template('sparql/sparql.html', title='SPARQL',
                           form=form, result=result)
