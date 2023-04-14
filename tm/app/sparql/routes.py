import time
from flask import render_template, flash, request, current_app
import json
from app.sparql.forms import SPARQLForm, DataCategoryForm
from app.sparql import bp
from .fuseki import Fuseki
from .query import SyntheaQueryGuiFactory, SyntheaQueryApiFactory
from .policymanager import DUAPolicyManager
from .duapolicy import DUAPolicy

# from .user import UserInfo


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


@bp.route("/api", methods=["GET", "POST"])
def query_patient_api():
    """
    TODO:
        - Add 403 error handling when the user is not allowed to access the data.
    """
    # Get parameters
    category = request.args.get("category").capitalize()
    condition = request.args.get("condition")
    user_id = request.args.get("user_id")
    data_custodian = request.args.get("data_custodian")

    fuseki = Fuseki()
    duaPolicyManager = DUAPolicyManager()

    # Policy
    st = time.time()
    dua_policy = DUAPolicy()
    isDuaCompliant = fuseki.ask(dua_policy.dua_existence(user_id))
    isRequestedDataMatched = fuseki.ask(
        dua_policy.match_requested_data(user_id, category)
    )
    et = time.time()
    policy_time = et - st
    if not isDuaCompliant or not isRequestedDataMatched:
        current_app.logger.info(
            f"{user_id}'s access to {category} data is not allowed."
        )
        current_app.logger.info(f"Policy processing time: {policy_time}")
        return (
            "Unavailable for legal reasons.",
            451,
        )
    else:
        current_app.logger.info(f"Access to {category} data is allowed.")

    # Query
    st = time.time()
    query_factory = SyntheaQueryApiFactory(category=category, condition=condition)
    query = query_factory.get_select_query()
    isExist = fuseki.ask(query_factory.get_ask_existence_query())
    result = fuseki.query(query, format="json")
    et = time.time()
    elapsed_time = et - st
    total_count = len(result["results"]["bindings"])
    # if not isExist and total_count > 0:
    #     current_app.logger.info(f"Access to {category} data is not allowed.")
    # else:
    #     current_app.logger.info(f"Access to {category} data is allowed.")
    # {"count": total_count, "result": result, "query": query, "elapsed_time": elapsed_time}
    return json.dumps(
        {
            "count": total_count,
            "query": query,
            "elapsed_time": elapsed_time,
            "result": result["results"]["bindings"],
        }
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
