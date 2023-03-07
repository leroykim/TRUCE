from flask_wtf import FlaskForm
from .formdata import get_score_weights
from .user import UserInfo
from SPARQLBurger.SPARQLQueryBuilder import Prefix, Triple, SPARQLSelectQuery, SPARQLGraphPattern, Filter

class DUAPolicyManager ():
    def __init__(self):
        self.user_info = UserInfo()

    def get_dua_policy(self):
        individual_id = self.user_info.individual_id
        dua_pattern = SPARQLGraphPattern()
        dua_pattern.add_triples(
            triples=[
                Triple(subject=f"syn:{individual_id}", predicate="syn:belongsTo", object="?organization"),
                Triple(subject="?dua", predicate="dua:hasDataCustodian", object="?dataCustodian"),
                Triple(subject="?dua", predicate="dua:hasRecipient", object="?recipient"),
                Triple(subject="?dua", predicate="dua:requestedData", object="?data")
            ]
        )
        dua_pattern.add_filter(
            filter = Filter(
                expression = "STR(?dataCustodian) = STR(syn:organization_a170b742-0340-37b8-9fd4-e9918aba0537)"
            )
        )
        dua_pattern.add_filter(
            filter = Filter(
                expression= "STR(?data) IN ()"
            )
        )


class TrustPolicyManager():
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

    def get_veracity_policy(self, datatype: str = "observation", result_variable: str = "veracity_weighted_average") -> str:
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

    def get_veracity_triples(self, datatype:str):
        where_clause = self.__get_veracity_where_pattern(datatype=datatype).get_text()
        return self.__strip_curly_brackets(where_clause)

    def __get_veracity_where_pattern(self, datatype: str):
        where_pattern = SPARQLGraphPattern()
        subject = f"?{datatype.lower()}"
        where_pattern.add_triples(
            triples=[
                Triple(subject=subject, predicate="tst:credibility",
                       object="?credibility"),
                Triple(subject=subject, predicate="tst:objectivity",
                       object="?objectivity"),
                Triple(subject=subject, predicate="tst:trustfulness",
                       object="?trustfulness"),
            ]
        )
        return where_pattern

    def __strip_curly_brackets(self, clause: str):
        clause = clause.replace('   ', '')
        clause = clause.replace('{', '')
        clause = clause.replace('}', '')
        return clause.strip()