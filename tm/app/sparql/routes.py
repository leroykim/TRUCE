import time
from flask import render_template, flash, request, current_app, g
import json
from app.sparql.forms import SPARQLForm, DataCategoryForm
from app.sparql import bp
from app.trust.trustmanager import TrustManager
from app.sparql.fuseki import Fuseki
from app.sparql.query import SyntheaQueryGuiFactory, SyntheaQueryApiFactory
from app.policy.policychecker import DUAPolicyChecker


@bp.route("/api", methods=["GET", "POST"])
def query_api():
    # Get parameters
    category = request.args.get("category").capitalize()
    condition = request.args.get("condition")
    user_id = request.args.get("user_id")
    # data_custodian = request.args.get("data_custodian")

    if not user_id:
        return "User ID is required.", 400

    if not category:
        return "Category is required.", 400

    # Policy check
    duaPolicyChecker = DUAPolicyChecker()
    trustManager = TrustManager()

    # Policy against data recipient
    isCompliant, dua_result = duaPolicyChecker.checkDataRecipient(user_id, category)
    trustManager.update(user_id, dua_result)
    if not isCompliant:
        return (
            "Unavailable for legal reasons.",
            451,
        )

    # Policy against data custodian
    isCompliant, dua_result = duaPolicyChecker.checkDataCustodian(category)
    trustManager.update("user_data_custodian", dua_result)
    if not isCompliant:
        return (
            "Service Unavailable.",
            503,
        )

    # Query
    fuseki = Fuseki()
    query_factory = SyntheaQueryApiFactory(category=category, condition=condition)
    query = query_factory.get_select_query()
    result = fuseki.query(query, format="json")
    total_count = len(result["results"]["bindings"])

    return json.dumps(
        {
            "count": total_count,
            "query": query,
            "result": result["results"]["bindings"],
        }
    )


@bp.route("/api/elapsed_time", methods=["GET"])
def get_elapsed_time():
    return json.dumps(
        {
            "recipient_policy_check_time": current_app.config[
                "RECIPIENT_POLICY_CHECK_TIME"
            ],
            "custodian_policy_check_time": "not implemented yet",
            "trust_update_time": current_app.config["TRUST_UPDATE_TIME"],
            "query_time": current_app.config["QUERY_TIME"],
        }
    )


@bp.route("/", methods=["GET", "POST"])
@bp.route("/data", methods=["GET", "POST"])
def query_patient():
    form = DataCategoryForm()
    if form.validate_on_submit():
        flash("SPARQL query has been sent.")

        st = time.time()
        query_factory = SyntheaQueryGuiFactory(form=form)
        fuseki = Fuseki()
        query = query_factory.get_select_query()
        result = fuseki.query(query)
        et = time.time()
        elapsed_time = et - st

        # For informations
        # user_info = UserInfo()
        # user_trust_score = f"{user_info.individual_id}'s identity score: {user_info.get_identity_score()} & behavior score: {user_info.get_behavior_score()}, query elapsed time: {elapsed_time} seconds"
        # query_for_html = query.replace("<", "&lt;").replace(">", "&gt;")
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


@bp.route("/experiment", methods=["GET", "POST"])
def run_experiment():
    category = request.args.get("category")
    condition = request.args.get("condition")
    endurance = request.args.get("endurance")
    incidents = []
    st = time.time()
    query_factory = SyntheaQueryApiFactory(category=category, condition=condition)
    query = query_factory.get_select_query()
    fuseki = Fuseki()
    for i in range(int(endurance)):
        isExist = fuseki.ask(query_factory.get_ask_existence_query())
        result = fuseki.query(query, format="json")
        total_count = len(result["results"]["bindings"])
        if isExist and total_count == 0:
            incidents.append(-1)
        else:
            incidents.append(1)
    et = time.time()
    elapsed_time = et - st
    # {"count": total_count, "result": result, "query": query, "elapsed_time": elapsed_time}
    return {
        "isExist": isExist,
        "count": total_count,
        "incidents": incidents,
        "query": query,
        "elapsed_time": elapsed_time,
    }


@bp.route("/sparql", methods=["GET", "POST"])
def query_sparql():
    form = SPARQLForm()
    if form.validate_on_submit():
        flash("SPARQL query has been sent.")
        fuseki = Fuseki()
        result = fuseki.query(form.sparql_query.data)
    else:
        result = None
    return render_template(
        "sparql/sparql.html", title="SPARQL", form=form, result=result
    )


# @bp.route('/setting', methods=['GET', 'POST'])
# @login_required
# def setting():
#     form = SettingForm()
#     return render_template('sparql/setting.html', title='Setting', form=form)
