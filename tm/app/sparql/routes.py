from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
from app.sparql.forms import SPARQLForm, PatientDataForm
from app.sparql import bp
from .fuseki import Fuseki
from .query import QueryFactory
from .user import UserInfo

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/data', methods=['GET', 'POST'])
@login_required
def query_patient():
    form = PatientDataForm()
    if form.validate_on_submit():
        flash('SPARQL query has been sent.')
        patient_query_factory = QueryFactory(form=form, data_class="patient")
        fuseki = Fuseki()
        ask_query = patient_query_factory.get_ask_query()
        available_endpoint_list = fuseki.ask_all(ask_query)
        
        user_info = UserInfo()

        query = patient_query_factory.get_federated_query(available_endpoint_list, policy=True)
        result = fuseki.query(query)
    else:
        result = None
    return render_template('sparql/patient.html', title='PATIENT DATA',
                           form=form, result=result)


@bp.route('/sparql', methods=['GET', 'POST'])
@login_required
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

# @bp.route('/setting', methods=['GET', 'POST'])
# @login_required
# def setting():
#     form = SettingForm()
#     return render_template('sparql/setting.html', title='Setting', form=form)