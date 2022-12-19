from flask_wtf import FlaskForm
from flask import current_app
from .formdata import get_patient_selection
from SPARQLBurger.SPARQLQueryBuilder import SPARQLGraphPattern, Triple


class QueryFactory():
    def __init__(self, form: FlaskForm):
        self.form = form
        self.prefix = None
        self.variable_list = None
        self.select = None
        self.where = None
        self.federated = None
        self.sparql_query = form.sparql_query.data

    def get_select_patient_query(self):
        self.__get_prefix()
        self.__get_variable_list(get_patient_selection)
        self.__set_select_clause("Patient")
        self.__set_where_clause("Patient")
        query = '\n'.join([self.prefix, self.select, self.where])
        return query

    def get_ask_patient_query(self):
        self.__get_prefix()
        self.__get_variable_list(get_patient_selection)
        self.__set_where_clause("Patient")
        query = '\n'.join([self.prefix, "ASK", self.where])
        return query

    def get_federated_patient_query(self, available_endpoint_list):
        self.__get_prefix()
        self.__get_variable_list(get_patient_selection)
        self.__set_select_clause("Patient")
        self.__set_federated_clause(available_endpoint_list)
        query = '\n'.join([
            self.prefix,
            self.select, 
            self.__wrap_where(self.federated)
            ])
        return query

    def __get_prefix(self):
        prefix_list = list(current_app.config['PREFIX_LIST'])
        self.prefix = '\n'.join(["PREFIX " + i for i in prefix_list])

    def __get_variable_list(self, func):
        selection = func(self.form)
        self.variable_list = []
        for key, value in selection.items():
            if value:
                self.variable_list.append(key)

    def __set_select_clause(self, type: str):
        sparql_variable_list = [f"?{type.lower()}"]
        sparql_variable_list.extend(["?" + i for i in self.variable_list])
        self.select = f"SELECT " + ' '.join(sparql_variable_list)

    def __set_where_clause(self, type: str):
        """Creates WHERE clause for non-federated query

        Args:
            type: type of the data. E.g. syn:Patient, syn:Encounter, ...
        """
        sparql_query = self.form.sparql_query.data
        variable_triple_list = [
            f"?{type.lower()} syn:{i} ?{i} ." for i in self.variable_list]
        variable_triple_string = '\n'.join(variable_triple_list)
        self.where = '\n'.join([
            "WHERE {",
            f"?{type.lower()} a syn:{type.capitalize()} .",
            variable_triple_string,
            sparql_query,
            "}"
        ])

    def __set_federated_clause(self, available_endpoint_list: list):
        """Creates federated clause of SPARQL query consists of UNION and SERVI-
        CE clauses

        Args:
            available_endpoint_list: list of endpoints that have desired data.

        """
        federated_clause = '\n'.join(['{', self.sparql_query, '}'])
        for endpoint in available_endpoint_list:
            federated_clause += self.__union_service_pattern(endpoint,
                                                             self.sparql_query)
        self.federated = federated_clause

    def __union_service_pattern(self, endpoint: str):
        pattern = '\n'.join([
            "UNION {",
            f"SERVICE <{endpoint}> {{",
            self.sparql_query,
            "}}", ])

    def __wrap_where(self, sparql_query:str):
        return '\n'.join('WHERE {', sparql_query, '}')

    def get_policy():
        ...
