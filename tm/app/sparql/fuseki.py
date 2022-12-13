from rdflib import Namespace
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

class FusekiConnector():
    def __init__(self, endpoint, ontology_iri, namespace_abbr):
        self.endpoint = endpoint
        self.namespace = Namespace(ontology_iri)
        self.namespace_abbr = namespace_abbr
        self.store = None
        self.connect()

        # QUERY_ENDPOINT = 'http://localhost:3031/maryland_covid/query'
        # UPDATE_ENDPOINT = 'http://localhost:3031/maryland_covid/update'
        # ONTOLOGY_IRI = "https://knacc.umbc.edu/leroy/ontologies/synthea#"
        # SYN = Namespace(ONTOLOGY_IRI)

    def connect(self):
        self.store = SPARQLUpdateStore()
        query_endpoint = f"{self.endpoint}/query"
        update_endpoint = f"{self.endpoint}/update"
        self.store.open((query_endpoint, update_endpoint))
        self.store.bind(self.namespace_abbr, self.namespace)

    def query(self, query):
        result = self.store.query(query)
        return result

        # query = '''
        #     PREFIX syn: <https://knacc.umbc.edu/leroy/ontologies/synthea#>

        #     SELECT ?patient
        #     WHERE {
        #       ?patient a syn:Patient.
        #     }
        # '''
