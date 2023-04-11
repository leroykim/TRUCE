from abc import ABC, abstractmethod
from SPARQLBurger.SPARQLQueryBuilder import SPARQLGraphPattern, Triple
from query import SPARQLAskQuery


class AccessPolicy(ABC):
    @abstractmethod
    def __init__(self):
        self.count = None
        self.policies = None

    @property
    @abstractmethod
    def count(self) -> int:
        pass

    @property
    @abstractmethod
    def policies(self) -> list[str]:
        pass


class DUAPolicy(AccessPolicy):
    def __init__(self):
        self.count = 2
        self.policies = ["dua_existence", "match_requested_data"]

    def count(self) -> int:
        return self.count

    def policies(self) -> list[str]:
        return self.policies

    def dua_existence(self, user_label: str):
        existence_pattern = SPARQLGraphPattern()
        existence_pattern.add_triples(
            triples=[
                Triple(
                    subject="?dataCustodian",
                    predicate="a",
                    object="syn:Organization",
                ),
                Triple(
                    subject="?dataCustodian",
                    predicate="rdfs:label",
                    object="?DataCustodian",
                ),
                Triple(
                    subject="?user",
                    predicate="a",
                    object="tst:User",
                ),
                Triple(
                    subject="?user",
                    predicate="rdfs:label",
                    object=f'"{user_label}"^^rdf:PlainLiteral',
                ),
                Triple(
                    subject="?user",
                    predicate="syn:affiliatedWith",
                    object="?organization",
                ),
                Triple(
                    subject="?dua",
                    predicate="a",
                    object="dua:DataUseAgreement",
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
        )
        ask_query = SPARQLAskQuery()
        ask_query.set_pattern(existence_pattern)
        return ask_query.get_text()

    def match_requested_data(self, user_label: str):
        ...
