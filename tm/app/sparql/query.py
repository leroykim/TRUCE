from flask_wtf import FlaskForm
from flask import current_app
from SPARQLBurger.SPARQLQueryBuilder import SPARQLSelectQuery, Prefix
from . import policy
from . import formdata
from . import triple


class SyntheaQueryFactory:
    def __init__(self, form: FlaskForm):
        self.form = form
        self.user_query = form.sparql_query.data
        self.data_category_selections = formdata.get_data_category_selections(form=form)
        # self.trust_policy_manager = policy.TrustPolicyManager(form=form)
        self.limit = formdata.get_limit(form=form)

    def get_select_query(self):
        # Gather necessary information
        prefix_list = current_app.config["PREFIX_DICT"]
        variable_list = triple.get_variables(data_category_selection=self.data_category_selections)
        data_property_pattern = triple.get_data_properties(data_category_selection=self.data_category_selections)
        # Build select query
        select_query = SPARQLSelectQuery()
        for prefix, namespace in prefix_list.items():
            select_query.add_prefix(prefix=Prefix(prefix=prefix, namespace=namespace))
        select_query.add_variables(variables=variable_list)
        select_query.set_where_pattern(graph_pattern=data_property_pattern)
        current_app.logger.info(select_query.get_text())
