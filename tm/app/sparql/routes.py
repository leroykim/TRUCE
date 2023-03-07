import time
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from app.sparql.forms import SPARQLForm, DataCategoryForm
from app.sparql import bp
from .fuseki import Fuseki
from .query import QueryFactory
from .user import UserInfo


@bp.route("/", methods=["GET", "POST"])
@bp.route("/data", methods=["GET", "POST"])
def query_patient():
    form = DataCategoryForm()
    if form.validate_on_submit():
        flash("SPARQL query has been sent.")

        st = time.time()
        # query_factory = QueryFactory(form=form, data_class="patient")
        fuseki = Fuseki()
        # ask_query = query_factory.get_ask_query()
        # available_endpoint_list = fuseki.ask_all(ask_query)
        # query = query_factory.get_federated_query(available_endpoint_list)
        # query = query_factory.get_select_query()
        result = fuseki.query(query)
        et = time.time()
        elapsed_time = et - st

        # For informations
        user_info = UserInfo()
        user_trust_score = f"{user_info.individual_id}'s identity score: {user_info.get_identity_score()} & behavior score: {user_info.get_behavior_score()}, query elapsed time: {elapsed_time} seconds"
        query_for_html = query.replace("<", "&lt;").replace(">", "&gt;")
    else:
        result = None
        query = None
        query_for_html = None
        user_trust_score = None

    return render_template(
        "sparql/patient.html",
        title="PATIENT DATA",
        form=form,
        result=result,
        query=query_for_html,
        user_trust_score=user_trust_score,
    )


@bp.route("/sparql", methods=["GET", "POST"])
def query_sparql():
    form = SPARQLForm()
    if form.validate_on_submit():
        flash("SPARQL query has been sent.")
        fuseki = Fuseki()
        result = fuseki.query(form.sparql_query.data)
    else:
        result = None
    return render_template("sparql/sparql.html", title="SPARQL", form=form, result=result)


# @bp.route('/setting', methods=['GET', 'POST'])
# @login_required
# def setting():
#     form = SettingForm()
#     return render_template('sparql/setting.html', title='Setting', form=form)
