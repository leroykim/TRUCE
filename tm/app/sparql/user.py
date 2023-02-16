from flask import current_app
from SPARQLBurger.SPARQLQueryBuilder import Prefix, Triple, SPARQLSelectQuery, SPARQLGraphPattern
from .fuseki import Fuseki

class UserInfo():
    def __init__(self):
        self.fuseki = Fuseki()
        self.individual_id = current_app.config['INDIVIDUAL_ID']
        self.user_type = current_app.config['INDIVIDUAL_TYPE']
        self.identity_trust = None
        self.behavioral_trust = None
        current_app.logger.info(f"User individual id = {self.individual_id}")

        self.__get_trust_score()

    def get_identity_score(self):
        if self.identity_trust:
            return self.identity_trust
        else:
            return None
    
    def get_behavior_score(self):
        if self.behavioral_trust:
            return self.behavioral_trust
        else:
            return None

    def get_trust_triples(self):
        where_clause = self.__get_trust_where_pattern().get_text()
        return self.__strip_curly_brackets(where_clause)

    def __get_trust_where_pattern(self):
        where_pattern = SPARQLGraphPattern()
        where_pattern.add_triples(
            triples=[
                Triple(subject=self.individual_id, predicate="a", object=f"syn:{self.user_type}"),
                Triple(subject=self.individual_id, predicate="tst:identity", object="?identity_trust"),
                Triple(subject=self.individual_id, predicate="tst:behavior", object="?behavioral_trust"),
            ]
        )
        return where_pattern

    def __get_trust_score(self):
        query = self.__get_trust_query()
        current_app.logger.info(query)
        user_info = self.fuseki.query(query, format='json')

        bindings = user_info["results"]["bindings"][0]
        self.identity_trust = bindings['identity_trust']['value']
        self.behavioral_trust = bindings['behavioral_trust']['value']
        
        current_app.logger.info(f"\nUser info query = \n{query}")
        current_app.logger.info(f"User's identity trust score = {self.identity_trust}")
        current_app.logger.info(f"User's behavioral trust score = {self.behavioral_trust}")

    def __get_trust_query(self):
        select_query = SPARQLSelectQuery(distinct=True)
        select_query.add_prefix(
            Prefix(prefix='syn', namespace='https://knacc.umbc.edu/leroy/ontologies/synthea#')
        )
        select_query.add_prefix(
            Prefix(prefix='tst', namespace='https://knacc.umbc.edu/leroy/ontologies/trust#')
        )
        select_query.add_variables(variables=["?identity_trust", "?behavioral_trust"])
        where_pattern = self.__get_trust_where_pattern()
        select_query.set_where_pattern(graph_pattern=where_pattern)

        return select_query.get_text()

    def __strip_curly_brackets(self, clause: str):
        clause = clause.replace('   ','')
        clause = clause.replace('{','')
        clause = clause.replace('}','')
        return clause.strip()