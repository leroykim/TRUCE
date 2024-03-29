import time
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from flask import current_app
from tempfile import NamedTemporaryFile
from pandas import read_csv
from tabulate import tabulate
import json


class Fuseki:
    """
    This class should ONLY be used to query the Fuseki server.
    Do not add features outside of this scope.
    """

    def __init__(self):
        endpoint = current_app.config["FUSEKI_URL"]
        self.store = SPARQLUpdateStore()
        self.query_endpoint = f"{endpoint}/query"
        self.update_endpoint = f"{endpoint}"
        self.store.open((self.query_endpoint, self.update_endpoint))

        # self.remote_endpoint_list = current_app.config['REMOTE_URL_DICT']

    """
    SELECT DISTINCT ?user ?label
WHERE {
  ?user rdf:type tst:User .
  ?user rdfs:label ?label .
}
    """

    def query_with_time(self, sparql_query, format="html"):
        st = time.time()
        print(f"Fuseki URL: {self.query_endpoint}")
        print(f"Query sent:\n{sparql_query}")
        result = self.store.query(sparql_query)
        # current_app.logger.info(json.loads(result.serialize(format='json')))
        if format == "html":
            result = self.__get_html(result)
        elif format == "text":
            result = self.__get_text(result)
        elif format == "json":
            result = json.loads(result.serialize(format="json"))
        query_time = time.time() - st
        if not current_app.config["QUERY_TIME"]:
            current_app.config["QUERY_TIME"] = (query_time, 1)
        else:
            current_app.config["QUERY_TIME"] = (
                current_app.config["QUERY_TIME"][0] + query_time,
                current_app.config["QUERY_TIME"][1] + 1,
            )
        count = len(result["results"]["bindings"])
        current_app.logger.info(f"Total {count} results retrieved.")
        return result

    def query(self, sparql_query):
        result = self.store.query(sparql_query)
        result = json.loads(result.serialize(format="json"))
        count = len(result["results"]["bindings"])
        current_app.logger.info(f"Total {count} results retrieved.")
        return result

    def query_user_trustscore(self, user_id):
        pass

    def query_org_trustscore(self, org_id):
        pass

    def update(self, sparql_query):
        self.store.update(sparql_query)

    def ask(self, ask_query):
        # print(f"Query sent:\n{ask_query}")
        result = self.store.query(ask_query)
        result_json = json.loads(result.serialize(format="json"))
        return result_json["boolean"]

    def ask_remote(self, remote_endpoint, ask_query):
        store = SPARQLUpdateStore()
        store.open((f"{remote_endpoint}/query", f"{remote_endpoint}/update"))
        result = store.query(ask_query)
        result_json = json.loads(result.serialize(format="json"))
        return result_json["boolean"]

    def ask_all(self, ask_query):
        result_list = []
        for endpoint, alias in self.remote_endpoint_list.items():
            result = self.ask_remote(endpoint, ask_query)
            if result:
                result_list.append(alias)
        current_app.logger.info(f"Available URL list:\n{result_list}")
        return result_list

    def __get_html(self, result):
        temp = NamedTemporaryFile()
        result.serialize(destination=temp.name, format="csv")
        df = read_csv(temp.name)
        temp.close()
        html = df.to_html(classes="table")
        return html

    def __get_text(self, result):
        temp = NamedTemporaryFile()
        result.serialize(destination=temp.name, format="csv")
        df = read_csv(temp.name)
        temp.close()
        table = tabulate(df, headers="keys", tablefmt="psql")
        return table
