from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import current_user, login_required
from app.sparql.forms import SPARQLForm, PatientDataForm
from app.sparql import bp
from .fuseki import Fuseki
from .query import QueryFactory


@bp.route('/data', methods=['GET', 'POST'])
def query_patient():
    form = PatientDataForm()
    if form.validate_on_submit():
        flash('SPARQL query has been generated.')
        factory = QueryFactory(form, "patient")
        fuseki = Fuseki()
        ask_query = factory.ask_patient_query()
        available_endpoint_list = fuseki.ask_all(ask_query)
        query = factory.federated_patient_query(available_endpoint_list)
        print(query)
        #query = factory.get_select_patient_query()
        result = fuseki.query(query)
    else:
        result = None
    return render_template('sparql/patient.html', title='PATIENT DATA',
                           form=form, result=result)


@bp.route('/sparql', methods=['GET', 'POST'])
def query_sparql():
    form = SPARQLForm()
    if form.validate_on_submit():
        flash('SPARQL query has been sent.')
        fuseki = Fuseki()
        result = fuseki.query(form.sparql_query.data)
    else:
        result = None
    return render_template('sparql/sparql.html', title='SPARQL',
                           form=form, result=result)
