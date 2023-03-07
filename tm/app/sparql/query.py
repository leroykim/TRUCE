from collections import OrderedDict
from flask_wtf import FlaskForm
from flask import current_app
from .policy import TrustPolicyManager
from .formdata import get_patient_selections, get_observation_selections


class QueryFactory():
    def __init__(self, form: FlaskForm, data_class: str):
        self.form = form
        self.user_query = form.sparql_query.data
        self.variables = OrderedDict()
        self.variables["patient"] = get_variables(form, get_patient_selections)
        self.variables["observation"] = get_variables(
            form, get_observation_selections)
        self.trust_policy_manager = TrustPolicyManager(form=form)
        self.limit = form.limit.data

    def get_select_query(self):
        prefix = get_prefix()
        select = get_select_clause(variables=self.variables)
        where = get_where_clause(variables=self.variables)
        query = '\n'.join([prefix, select, where])
        current_app.logger.info(query)
        return query

    def get_ask_query(self):
        prefix = get_prefix()
        where = get_where_clause(self.variables)
        query = '\n'.join([prefix, "ASK", where])
        # current_app.logger.info(f"\n{query}")
        return query

    def get_federated_query(self, endpoint_list):
        if endpoint_list is None:
            print("endpoint_list is empty")
            return

        policies = []
        policy_variables = []
        if self.trust_policy_manager.is_trust_policy_requested():
            policies.append(self.trust_policy_manager.get_trust_policy())
            policy_variables.append("trust_weighted_average")
        if self.trust_policy_manager.is_veracity_policy_requested():
            policies.append(self.trust_policy_manager.get_veracity_policy())
            policy_variables.append("veracity_weighted_average")

        prefix = get_prefix()
        select = get_select_clause(
            variables=self.variables, additional_variables=["veracity_weighted_average"])
        federated = get_federated_clause(
            endpoints=endpoint_list, variables=self.variables, condition_query=self.user_query, policies=policies)
        
        query_component = [prefix, select, wrap_where(federated)]
        if self.limit:
            query_component.append(f"LIMIT {self.limit}")
        query = '\n'.join(query_component)
        current_app.logger.info(f"\n{query}")
        return query


def get_prefix() -> str:
    prefix_list = list(current_app.config['PREFIX_LIST'])
    return '\n'.join(["PREFIX " + i for i in prefix_list])


def get_variables(form: FlaskForm, selection_method: callable) -> list:
    form_data = selection_method(form)
    variable_list = []
    for key, value in form_data.items():
        if value:
            variable_list.append(key)
    return variable_list


def get_select_clause(variables: dict[str, list], distinct=True, additional_variables: list = None) -> str:
    sparql_variable_list = []
    for data_class, variable_list in variables.items():
        if variable_list:
            sparql_variable_list.append(f"?{data_class.lower()}")
            sparql_variable_list.extend(["?" + i for i in variable_list])
    #sparql_variable_list = [f"?{i.lower()}" for i in variables.keys()]
    #sparql_variable_list.extend(["?" + i for i in variables])
    if additional_variables:
        sparql_variable_list.extend(["?" + i for i in additional_variables])
    if distinct:
        return f"SELECT DISTINCT " + ' '.join(sparql_variable_list)
    else:
        return f"SELECT " + ' '.join(sparql_variable_list)


def get_triples(variables: dict[str, list], condition_query: str = None) -> str:
    triple_list = []
    for datatype, variable_list in variables.items():
        if variable_list:
            if datatype == 'observation':
                triple_list.append("?observation syn:observedPatient ?patient .")
            triple_list.append(
                f"?{datatype.lower()} a syn:{datatype.capitalize()} .")
            triple_list.extend(
                [f"?{datatype.lower()} syn:{i} ?{i} ." for i in variable_list])
    if condition_query:
        triple_list.append(condition_query)
    triple_string = '\n'.join(triple_list)
    print(f"triple_string = {triple_string}")
    return triple_string


def get_where_clause(variables: dict[str, list], condition_query: str = None):
    return wrap_where(get_triples(variables=variables, condition_query=condition_query))


def get_federated_clause(endpoints: list, variables: dict[str, list], condition_query: str = None, policies: list = None):
    triples = get_triples(variables=variables, condition_query=condition_query)
    federated_clause = '\n'.join(['{', triples, '}'])
    for endpoint in endpoints:
        federated_clause += wrap_union_service(endpoint, triples)
    if policies:
        for policy in policies:
            federated_clause = '\n'.join([federated_clause, policy])
    return federated_clause


def wrap_where(triples: str) -> str:
    return '\n'.join(['WHERE {', triples, '}'])


def wrap_union_service(endpoint: str, triples: str) -> str:
    pattern = '\n'.join([
        "UNION {",
        f"SERVICE <{endpoint}> {{",
        triples,
        "}}", ])
    return pattern
