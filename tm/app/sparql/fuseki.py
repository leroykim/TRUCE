from rdflib import Namespace
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from flask import current_app

class FusekiConnector():
    def __init__(self):
        self.endpoint = current_app.config['FUSEKI_URL']
        self.ontology_iri = current_app.config['ONTOLOGY_IRI']
        self.namespace_abbr = current_app.config['NAMESPACE_ABR']
        self.namespace = Namespace(self.ontology_iri)
        self.store = None
        self.connect()

    def connect(self):
        self.store = SPARQLUpdateStore()
        query_endpoint = f"{self.endpoint}/query"
        update_endpoint = f"{self.endpoint}/update"
        self.store.open((query_endpoint, update_endpoint))
        self.store.bind(self.namespace_abbr, self.namespace)

    def query(self, query):
        result = self.store.query(query)
        for row in result:
            print(f"{row.patient}")
        return result

        # query = '''
        #     PREFIX syn: <https://knacc.umbc.edu/leroy/ontologies/synthea#>

        #     SELECT ?patient
        #     WHERE {
        #       ?patient a syn:Patient.
        #     }
        # '''

class QueryBuilder():
    # get arguments from the data form
    pass