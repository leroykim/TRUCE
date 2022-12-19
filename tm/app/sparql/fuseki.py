from rdflib import Namespace
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from flask import current_app
from tempfile import NamedTemporaryFile
from pandas import read_csv
from tabulate import tabulate
import json


class Fuseki():
    def __init__(self):
        endpoint = current_app.config['FUSEKI_URL']
        ontology_iri = current_app.config['ONTOLOGY_IRI']
        namespace_abbr = current_app.config['NAMESPACE_ABR']
        namespace = Namespace(ontology_iri)

        self.store = SPARQLUpdateStore()
        self.query_endpoint = f"{endpoint}/query"
        self.update_endpoint = f"{endpoint}/update"
        self.store.open((self.query_endpoint, self.update_endpoint))
        self.store.bind(namespace_abbr, namespace)

        self.tm_endpoint_list = current_app.config['OTHERS_URL']

    def query(self, sparql_query, format='html'):
        result = self.store.query(sparql_query)
        if format == 'html':
            return self.__get_html(result)
        elif format == 'text':
            return self.__get_text(result)

    def ask(self, sparql_query):
        result = self.store.query(sparql_query)
        result_json = json.loads(result.serialize(format='json'))
        return result_json['boolean']

    def federated(self, ask_query, select_query):
        available_endpoint_list = []
        for endpoint in self.tm_endpoint_list:
            available = self.ask(ask_query)
            if available:
                available_endpoint_list.append(endpoint)

    def __get_html(self, result):
        temp = NamedTemporaryFile()
        result.serialize(destination=temp.name, format='csv')
        df = read_csv(temp.name)
        temp.close()
        html = df.to_html(classes='table')
        return html

    def __get_text(self, result):
        temp = NamedTemporaryFile()
        result.serialize(destination=temp.name, format='csv')
        df = read_csv(temp.name)
        temp.close()
        table = tabulate(df, headers='keys', tablefmt='psql')
        return table
