from app.sparql.fuseki import Fuseki
from flask import current_app
from SPARQLBurger.SPARQLQueryBuilder import (
    SPARQLSelectQuery,
    SPARQLUpdateQuery,
    SPARQLGraphPattern,
    Triple,
)


class TrustManager:
    def __init__(self):
        self.fuseki = Fuseki()
        self.prefix_list = current_app.config["PREFIX_LIST"]

    def update(self, user_id: str, policy_result: dict[str, bool]):
        currunt_behavior_trust = self.__get_behavior_trust_score(user_id=user_id)
        new_behavior_trust = currunt_behavior_trust
        for key, value in policy_result.items():
            if value is False:
                current_app.logger.info(f"Policy {key} is not satisfied.")
                new_behavior_trust = new_behavior_trust - 0.01

        update_query = self.__get_update_trust_query(
            user_id, currunt_behavior_trust, new_behavior_trust
        )

        current_app.logger.info(update_query.get_text())

        self.fuseki.update(sparql_query=update_query.get_text())

    def __get_update_trust_query(self, user_id: str, current: float, new: float):
        update_query = SPARQLUpdateQuery()
        for prefix in self.prefix_list:
            update_query.add_prefix(prefix=prefix)
        delete_pattern = SPARQLGraphPattern()
        delete_pattern.add_triples(
            [
                Triple(
                    subject=f"?user",
                    predicate="tst:behaviorTrust",
                    object=f'"{current}"^^xsd:float',
                )
            ]
        )

        insert_pattern = SPARQLGraphPattern()
        insert_pattern.add_triples(
            [
                Triple(
                    subject=f"?user",
                    predicate="tst:behaviorTrust",
                    object=f'"{new}"^^xsd:float',
                )
            ]
        )

        where_pattern = SPARQLGraphPattern()
        where_pattern.add_triples(
            [
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
            ]
        )

        update_query.set_delete_pattern(delete_pattern)
        update_query.set_insert_pattern(insert_pattern)
        update_query.set_where_pattern(where_pattern)

        return update_query

    def __get_behavior_trust_score(self, user_id: str) -> float:
        select_query = SPARQLSelectQuery(distinct=True)
        triples = [
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
                predicate="tst:behaviorTrust",
                object="?behaviorTrust",
            ),
        ]
        pattern = SPARQLGraphPattern()
        pattern.add_triples(triples=triples)
        select_query.set_where_pattern(pattern)
        select_query.add_variables(variables=["?behaviorTrust"])
        for prefix in self.prefix_list:
            select_query.add_prefix(prefix=prefix)
        result = self.fuseki.query(sparql_query=select_query.get_text(), format="json")
        behavior_trust = result["results"]["bindings"][0]["behaviorTrust"]["value"]
        current_app.logger.info(f"{user_id}'s behaviorTrust: {behavior_trust}")
        return float(behavior_trust)