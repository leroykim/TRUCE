from rdflib import Namespace
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from flask import current_app
from tempfile import NamedTemporaryFile
from pandas import read_csv
from tabulate import tabulate

def query(sparql_query, format='text'):
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

    if format == 'text':
        return get_text(result)
    elif format == 'html':
        return get_html(result)

def get_text(result):
    temp = NamedTemporaryFile()
    result.serialize(destination=temp.name, format='csv')
    df = read_csv(temp.name)
    temp.close()
    table = tabulate(df, headers = 'keys', tablefmt = 'psql')
    return table

def get_html(result):
    temp = NamedTemporaryFile()
    result.serialize(destination=temp.name, format='csv')
    df = read_csv(temp.name)
    temp.close()
    html = df.to_html(classes='table')
    return html

class QueryBuilder():
    # get arguments from the data form
    pass