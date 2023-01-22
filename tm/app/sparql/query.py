from flask_wtf import FlaskForm
from flask import current_app
from .policy import PolicyManager
from .formdata import get_patient_variables

class QueryFactory():
    def __init__(self, form: FlaskForm, data_class: str):
        self.form = form
        self.user_query = form.sparql_query.data
        self.variables = get_variables(form)
        self.policy_manager = PolicyManager(form=form)
        self.data_class = data_class

    def get_select_query(self):
        prefix = get_prefix()
        select = get_select_clause(data_class=self.data_class, variables=self.variables)
        where = get_where_clause(data_class=self.data_class, sparql_query=self.user_query)
        query = '\n'.join([prefix, select, where])
        return query

    def get_ask_query(self):
        prefix = get_prefix()
        where = get_where_clause(
            data_class=self.data_class, variables=self.variables, sparql_query=self.user_query)
        query = '\n'.join([prefix, "ASK", where])
        # current_app.logger.info(f"\n{query}")
        return query

    def get_federated_query(self, endpoint_list, policy=False):
        if endpoint_list is None:
            print("endpoint_list is empty")
            return
        if policy:
            # This part should be changed later when many policies are defined.
            policies = [self.policy_manager.get_trust_policy()]
        federated = get_federated_clause(
            endpoints=endpoint_list, data_class=self.data_class, variables=self.variables, sparql_query=self.user_query, policies=policies)
        prefix = get_prefix()
        select = get_select_clause(data_class=self.data_class, variables=self.variables)
        query = '\n'.join([
            prefix,
            select,
            wrap_where(federated)
        ])
        current_app.logger.info(f"\n{query}")
        return query


def get_prefix() -> str:
    prefix_list = list(current_app.config['PREFIX_LIST'])
    return '\n'.join(["PREFIX " + i for i in prefix_list])


def get_variables(form: FlaskForm) -> list:
    form_data = get_patient_variables(form)
    variable_list = []
    for key, value in form_data.items():
        if value:
            variable_list.append(key)
    return variable_list


def get_select_clause(data_class: str, variables: list, distinct=True, additional_variables: list = None) -> str:
    sparql_variable_list = [f"?{data_class.lower()}"]
    sparql_variable_list.extend(["?" + i for i in variables])
    if additional_variables is not None:
        sparql_variable_list.extend(additional_variables)
    if distinct:
        return f"SELECT DISTINCT " + ' '.join(sparql_variable_list)
    else:
        return f"SELECT " + ' '.join(sparql_variable_list)


def get_triples(data_class: str, variables: list, sparql_query: str) -> str:
    variable_triple_list = [
        f"?{data_class.lower()} syn:{i} ?{i} ." for i in variables]
    variable_triple_string = '\n'.join(variable_triple_list)
    triples = '\n'.join([
        f"?{data_class.lower()} a syn:{data_class.capitalize()} .",
        variable_triple_string,
        sparql_query,
    ])
    return triples


def get_where_clause(data_class: str, variables: list, sparql_query: str, policy=False):
    """Creates WHERE clause for non-federated query

    Args:
        data_class: class of the data. E.g. syn:Patient, syn:Encounter, ...
    """
    return wrap_where(get_triples(data_class=data_class, variables=variables, sparql_query=sparql_query))


def get_federated_clause(endpoints: list, data_class: str, variables: list, sparql_query: str, policies: list = None):
    """Creates federated clause of SPARQL query consists of UNION and SERVI-
    CE clauses

    Args:
        endpoint_list: list of endpoints that have desired data.

    """
    triples = get_triples(data_class=data_class, variables=variables,
                          sparql_query=sparql_query)
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
