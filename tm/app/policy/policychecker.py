import time
from flask_wtf import FlaskForm
from app.sparql.formdata import get_score_weights
from app.sparql.user import UserInfo
from app.sparql.query import SPARQLAskQuery
from app.dua.duapolicy import DUAPolicy
from app.sparql.fuseki import Fuseki
from flask import current_app
from SPARQLBurger.SPARQLQueryBuilder import (
    Prefix,
    Triple,
    SPARQLSelectQuery,
    SPARQLGraphPattern,
    Filter,
)

"""
Since the policy manager was for many-to-many relationship, it should be changed to one-to-many relationship.
"""


class DUAPolicyChecker:
    """
    This class is for checking DUA policies.
    It sends a query to the triple store to check if the user is compliant with the DUA policy.
    """

    def __init__(self):
        # self.user_info = UserInfo()
        self.prefix_list = current_app.config["PREFIX_LIST"]
        self.duapolicy = DUAPolicy()
        self.fuseki = Fuseki()

    def check(self, user_id: str, requested_data: str):
        st = time.time()
        result_dict = dict()
        dua_existence = self.duapolicy.dua_existence(user_id=user_id)
        match_requested_data = self.duapolicy.match_requested_data(
            user_id=user_id, requested_data=requested_data
        )
        # match_permitted_usage_and_disclosure = (
        #     self.duapolicy.match_permitted_usage_and_disclosure(
        #         user_id=user_id, usage=usage
        #     )
        # )
        result_dict["dua_existence"] = self.fuseki.ask(ask_query=dua_existence)
        result_dict["match_requested_data"] = self.fuseki.ask(
            ask_query=match_requested_data
        )
        # result_dict["match_permitted_usage_and_disclosure"] = self.fuseki.ask(
        #     ask_query=match_permitted_usage_and_disclosure
        # )
        policy_time = time.time() - st
        current_app.logger.info(f"Policy processing time: {policy_time}")
        isCompliant = None
        for key, value in result_dict.items():
            current_app.logger.info(f"{key}: {value}")
            if not value:
                isCompliant = False
        return isCompliant, result_dict


class TrustPolicyManager:
    """
    Not used for now, but has useful methods.
    """

    def __init__(self, form: FlaskForm):
        self.score_weights = get_score_weights(form=form)
        self.user_info = UserInfo()

    def get_trust_policy(self, result_variable: str = "trust_weighted_average") -> str:
        trust_triples = self.user_info.get_trust_triples()
        identity_weight = self.score_weights["identity"]
        behavior_weight = self.score_weights["behavior"]
        trust_threshold = self.score_weights["trust_threshold"]
        bind_clause = f"BIND((xsd:float({identity_weight})*?identity_trust + xsd:float({behavior_weight})*?behavioral_trust) AS ?{result_variable})"
        filter_clause = f"FILTER(?{result_variable} >= xsd:float({trust_threshold}))"
        policy_clause = "\n".join([trust_triples, bind_clause, filter_clause])
        return policy_clause

    def get_veracity_policy(
        self,
        datatype: str = "observation",
        result_variable: str = "veracity_weighted_average",
    ) -> str:
        veracity_triples = self.get_veracity_triples(datatype=datatype)
        credibility_weight = self.score_weights["credibility"]
        objectivity_weight = self.score_weights["objectivity"]
        trustfulness_weight = self.score_weights["trustfulness"]
        veracity_threshold = self.score_weights["veracity_threshold"]
        bind_clause = f"BIND((xsd:float({credibility_weight})*?credibility + xsd:float({objectivity_weight})*?objectivity + xsd:float({trustfulness_weight})*?trustfulness) AS ?{result_variable})"
        filter_clause = f"FILTER(?{result_variable} >= xsd:float({veracity_threshold}))"
        policy_clause = "\n".join([veracity_triples, bind_clause, filter_clause])
        return policy_clause

    def is_trust_policy_requested(self):
        return self.score_weights["apply_trust_score"]

    def is_veracity_policy_requested(self, data_class: str = "observation"):
        return self.score_weights["apply_veracity_score"]

    def get_veracity_triples(self, datatype: str):
        where_clause = self.__get_veracity_where_pattern(datatype=datatype).get_text()
        return self.__strip_curly_brackets(where_clause)

    def __get_veracity_where_pattern(self, datatype: str):
        where_pattern = SPARQLGraphPattern()
        subject = f"?{datatype.lower()}"
        where_pattern.add_triples(
            triples=[
                Triple(
                    subject=subject,
                    predicate="tst:credibility",
                    object="?credibility",
                ),
                Triple(
                    subject=subject,
                    predicate="tst:objectivity",
                    object="?objectivity",
                ),
                Triple(
                    subject=subject,
                    predicate="tst:trustfulness",
                    object="?trustfulness",
                ),
            ]
        )
        return where_pattern

    def __strip_curly_brackets(self, clause: str):
        clause = clause.replace("   ", "")
        clause = clause.replace("{", "")
        clause = clause.replace("}", "")
        return clause.strip()
