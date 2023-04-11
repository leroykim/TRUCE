from flask_wtf import FlaskForm
from flask import current_app
from SPARQLBurger.SPARQLQueryBuilder import (
    SPARQLSelectQuery,
    Prefix,
    SPARQLGraphPattern,
)
from . import formdata
from . import triple


class SyntheaQueryGuiFactory:
    def __init__(self, form: FlaskForm):
        self.form = form
        self.user_query = form.sparql_query.data
        self.data_category_selections = formdata.get_data_category_selections(form=form)
        # self.trust_policy_manager = policy.TrustPolicyManager(form=form)
        self.limit = formdata.get_limit(form=form)

    def get_select_query(self):
        # Gather necessary information
        prefix_list = current_app.config["PREFIX_DICT"]
        variable_list = triple.get_variables(
            data_category_selection=self.data_category_selections
        )
        data_property_pattern = triple.get_data_properties(
            data_category_selection=self.data_category_selections
        )
        # Build select query
        select_query = SPARQLSelectQuery()
        for prefix, namespace in prefix_list.items():
            select_query.add_prefix(prefix=Prefix(prefix=prefix, namespace=namespace))
        select_query.add_variables(variables=variable_list)
        select_query.set_where_pattern(graph_pattern=data_property_pattern)
        current_app.logger.info(select_query.get_text())

        return select_query.get_text()


class SyntheaQueryApiFactory:
    def __init__(self, category: str, condition: str):
        """
        :param category: data category. e.g. "patient", "encounter", "observation", "condition", "procedure", "medication"
                        It should be dictionary in the form of {category: Boolean} e.g. {"patient": True, "encounter": False, ...
                        For now, only one category is allowed.
        :param condition: desired condition of the data in the form of triples.
        """
        self.category = {category: True}
        self.condition = condition

    def get_ask_existence_query(self):
        # Gather necessary information
        prefix_list = current_app.config["PREFIX_DICT"]
        data_property_pattern = triple.get_data_properties(
            data_category_selection=self.category
        )
        # Build ask query
        # TODO: This is a temporary solution. It should be changed to SPARQLAskQuery.
        ask_query = ""
        for prefix, namespace in prefix_list.items():
            ask_query += Prefix(prefix=prefix, namespace=namespace).get_text()
        ask_query += "ASK"
        ask_query += data_property_pattern.get_text()
        current_app.logger.info(ask_query)

        return ask_query

    def get_ask_query(self, graph_pattern: SPARQLGraphPattern):
        ask_query = SPARQLAskQuery()
        prefix_list = current_app.config["PREFIX_DICT"]
        for prefix, namespace in prefix_list.items():
            ask_query.add_prefix(prefix=Prefix(prefix=prefix, namespace=namespace))
        ask_query.set_pattern(graph_pattern=graph_pattern)

        return ask_query.get_text()

    def get_select_query(self):
        # Gather necessary information
        prefix_list = current_app.config["PREFIX_DICT"]
        variable_list = triple.get_variables(data_category_selection=self.category)
        data_property_pattern = triple.get_data_properties(
            data_category_selection=self.category
        )
        # Build select query
        select_query = SPARQLSelectQuery()
        for prefix, namespace in prefix_list.items():
            select_query.add_prefix(prefix=Prefix(prefix=prefix, namespace=namespace))
        select_query.add_variables(variables=variable_list)
        select_query.set_where_pattern(graph_pattern=data_property_pattern)
        current_app.logger.info(select_query.get_text())

        return select_query.get_text()


class SPARQLAskQuery:
    def __init__(self):
        self.prefix_list = []
        self.graph_pattern = None

    def add_prefix(self, prefix: Prefix):
        self.prefix_list.append(prefix)

    def set_pattern(self, graph_pattern: SPARQLGraphPattern):
        self.graph_pattern = graph_pattern

    def get_text(self):
        ask_query = ""
        for prefix in self.prefix_list:
            ask_query += prefix.get_text()
        ask_query += "ASK"
        ask_query += self.graph_pattern.get_text()
        current_app.logger.info(f"ASK query generated:\n{ask_query}")
        return ask_query
