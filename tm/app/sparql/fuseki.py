from rdflib import Namespace
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from flask import current_app

def query(sparql_query):
    endpoint = current_app.config['FUSEKI_URL']
    ontology_iri = current_app.config['ONTOLOGY_IRI']
    namespace_abbr = current_app.config['NAMESPACE_ABR']
    namespace = Namespace(ontology_iri)

    store = SPARQLUpdateStore()
    query_endpoint = f"{endpoint}/query"
    update_endpoint = f"{endpoint}/update"
    store.open((query_endpoint, update_endpoint))
    store.bind(namespace_abbr, namespace)

    result = store.query(sparql_query)
    for row in result:
        print(f"{row.patient}")
    return result

class QueryBuilder():
    # get arguments from the data form
    pass