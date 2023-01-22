from flask_wtf import FlaskForm
from .formdata import get_score_weights
from .user import UserInfo

class PolicyManager():
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

    def __get_veracity_policy(self, result_variable: str = "veracity_weighted_average") -> str:
        credibility_weight = self.score_weights["credibility"]
        objectivity_weight = self.score_weights["objectivity"]
        trustfulness_weight = self.score_weights["trustfulness"]
        veracity_threshold = self.score_weights["veracity_threshold"]
        bind_clause = f"BIND(({credibility_weight}*?credibility + {objectivity_weight}*?objectivity + {trustfulness_weight}*?trustfulness) AS ?{result_variable})"
        filter_clause = f"FILTER(?{result_variable} >= {veracity_threshold}^^xsd:float)"
        policy_clause = "\n".join([bind_clause, filter_clause])
        return policy_clause