import copy
from flask import current_app
from SPARQLBurger.SPARQLQueryBuilder import SPARQLGraphPattern, Triple
from app.policy.accesspolicy import AccessPolicy
from app.sparql.query import SPARQLAskQuery
from app.sparql.namespace import SYN


class DUAPolicy(AccessPolicy):
    def __init__(self):
        self.count = 2
        self.policies = ["dua_existence", "match_requested_data"]
        self.prefix_list = current_app.config["PREFIX_LIST"]

    def count(self) -> int:
        return self.count

    def policies(self) -> list[str]:
        return self.policies

    def dua_existence(self, user_id: str):
        existence_pattern = SPARQLGraphPattern()
        existence_pattern.add_triples(triples=self.default_triples(user_id=user_id))
        ask_query = self.default_query()
        ask_query.set_pattern(existence_pattern)
        return ask_query.get_text()

    def match_requested_data(self, user_id: str, requested_data: str):
        triples = copy.deepcopy(self.default_triples(user_id=user_id))
        triples.extend(
            [
                Triple(
                    subject="?dua",
                    predicate="dua:requestedData",
                    object=f'"{SYN[requested_data]}"^^rdf:PlainLiteral',
                ),
            ]
        )
        requested_data_pattern = SPARQLGraphPattern()
        requested_data_pattern.add_triples(triples=triples)
        ask_query = self.default_query()
        ask_query.set_pattern(requested_data_pattern)

        return ask_query.get_text()

    def match_permitted_usage_and_disclosure(self, user_id: str, usage: str):
        triples = copy.deepcopy(self.default_triples(user_id=user_id))
        triples.extend(
            [
                Triple(
                    subject="?dua",
                    predicate="dua:permittedUsage",
                    object=f'"{SYN[usage]}"^^rdf:PlainLiteral',
                ),
            ]
        )
        permitted_usage_pattern = SPARQLGraphPattern()
        permitted_usage_pattern.add_triples(triples=triples)
        ask_query = self.default_query()
        ask_query.set_pattern(permitted_usage_pattern)

        return ask_query.get_text()

    def default_triples(self, user_id: str) -> list[Triple]:
        return [
            Triple(
                subject="?dataCustodian",
                predicate="a",
                object="syn:Organization",
            ),
            Triple(
                subject="?dataCustodian",
                predicate="rdfs:label",
                object='"DataCustodian"^^rdf:PlainLiteral',
            ),
            Triple(
                subject="?user",
                predicate="a",
                object="tst:User",
            ),
            Triple(
                subject="?user",
                predicate="rdfs:label",
                object=f'"{user_id}"^^rdf:PlainLiteral',
            ),
            Triple(
                subject="?user",
                predicate="syn:isAffiliatedWith",
                object="?organization",
            ),
            Triple(
                subject="?dua",
                predicate="a",
                object="dua:DataUsageAgreement",
            ),
            Triple(
                subject="?dua",
                predicate="dua:hasRecipient",
                object="?organization",
            ),
            Triple(
                subject="?dua",
                predicate="dua:hasDataCustodian",
                object="?dataCustodian",
            ),
        ]

    def default_query(self) -> SPARQLAskQuery:
        ask_query = SPARQLAskQuery()
        for prefix in self.prefix_list:
            ask_query.add_prefix(prefix=prefix)
        return ask_query
