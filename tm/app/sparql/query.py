from flask_wtf import FlaskForm
from flask import current_app
from .formdata import get_patient_selection


class QueryFactory():
    def __init__(self, form: FlaskForm):
        self.tm_endpoint_list = current_app.config['OTHERS_URL']
        self.form = form
        self.prefix = None
        self.variable_list = None
        self.select = None
        self.where = None
        self.sparql_query = form.sparql_query.data

    def get_select_patient_query(self):
        self.__set_prefix()
        self.__set_variable_list(get_patient_selection)
        self.__set_select_clause("Patient")
        self.__set_patient_where_clause()
        query = '\n'.join([self.prefix, self.select, self.where])
        return query

    def get_patient_ask_query(self):
        self.__set_prefix()
        self.__set_variable_list(get_patient_selection)
        self.__set_patient_where_clause()
        query = '\n'.join([self.prefix, "ASK", self.where])
        return query

    def __set_prefix(self):
        prefix_list = list(current_app.config['PREFIX_LIST'])
        self.prefix = '\n'.join(["PREFIX " + i for i in prefix_list])

    def __set_variable_list(self, func):
        selection = func(self.form)
        self.variable_list = []
        for key, value in selection.items():
            if value:
                self.variable_list.append(key)

    def __set_select_clause(self, category:str):
        sparql_variable_list = [f"?{category.lower()}"]
        sparql_variable_list.extend(["?" + i for i in self.variable_list])
        self.select = f"SELECT " + ' '.join(sparql_variable_list)

    def __set_patient_where_clause(self):
        sparql_query = self.form.sparql_query.data
        variable_triple_list = [
            f"?patient syn:{i} ?{i} ." for i in self.variable_list]
        variable_triple_string = '\n'.join(variable_triple_list)
        self.where = '\n'.join([
            "WHERE {",
            "?patient a syn:Patient .",
            variable_triple_string,
            sparql_query,
            "}"
        ])

    def get_policy():
        ...
