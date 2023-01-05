from flask_wtf import FlaskForm
from flask import current_app
from .formdata import get_patient_selection
from SPARQLBurger.SPARQLQueryBuilder import SPARQLGraphPattern, Triple


class QueryFactory():
    def __init__(self, form: FlaskForm, type: str, distinct=True):
        self.form = form
        self.user_query = form.sparql_query.data
        self.prefix = self.__get_prefix()
        if type.lower() == "patient":
            self.variable_list = self.__get_variable_list(get_patient_selection)
        self.select = self.__get_select_clause(type)
        self.where = self.__get_where_clause(type)
        self.federated = None

    def select_patient_query(self):
        query = '\n'.join([self.prefix, self.select, self.where])
        return query

    def ask_patient_query(self):
        query = '\n'.join([self.prefix, "ASK", self.where])
        current_app.logger.info(f"\n{query}")
        return query

    def federated_patient_query(self, endpoint_list):
        if endpoint_list is None:
            print("endpoint_list is empty")
            return
        self.__set_federated_clause(endpoint_list, "patient")
        query = '\n'.join([
            self.prefix,
            self.select, 
            self.__wrap_where(self.federated)
            ])
        current_app.logger.info(f"\n{query}")
        return query

    def __get_prefix(self):
        prefix_list = list(current_app.config['PREFIX_LIST'])
        return '\n'.join(["PREFIX " + i for i in prefix_list])

    def __get_variable_list(self, func):
        selection = func(self.form)
        variable_list = []
        for key, value in selection.items():
            if value:
                variable_list.append(key)
        return variable_list

    def __get_select_clause(self, type: str, distinct=True):
        sparql_variable_list = [f"?{type.lower()}"]
        sparql_variable_list.extend(["?" + i for i in self.variable_list])
        if distinct:
            return f"SELECT DISTINCT " + ' '.join(sparql_variable_list)
        else:
            return f"SELECT " + ' '.join(sparql_variable_list)

    def __get_where_clause(self, type: str):
        """Creates WHERE clause for non-federated query

        Args:
            type: type of the data. E.g. syn:Patient, syn:Encounter, ...
        """
        triples = self.__get_triples(type)
        return self.__wrap_where(triples)


    def __set_federated_clause(self, endpoint_list: list, type: str):
        """Creates federated clause of SPARQL query consists of UNION and SERVI-
        CE clauses

        Args:
            endpoint_list: list of endpoints that have desired data.

        """
        triples = self.__get_triples(type)
        federated_clause = '\n'.join(['{', triples, '}'])
        for endpoint in endpoint_list:
            federated_clause += self.__union_service_pattern(endpoint, triples)
        self.federated = federated_clause

    def __get_triples(self, type:str):
        sparql_query = self.user_query
        variable_triple_list = [
            f"?{type.lower()} syn:{i} ?{i} ." for i in self.variable_list]
        variable_triple_string = '\n'.join(variable_triple_list)
        triples = '\n'.join([
            f"?{type.lower()} a syn:{type.capitalize()} .",
            variable_triple_string,
            sparql_query,
        ])
        return triples

    def __union_service_pattern(self, endpoint: str, triples: str):
        pattern = '\n'.join([
            "UNION {",
            f"SERVICE <{endpoint}> {{",
            triples,
            "}}", ])
        return pattern

    def __wrap_where(self, triples:str):
        return '\n'.join(['WHERE {', triples, '}'])

    def get_policy():
        ...
