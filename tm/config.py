import os
from dotenv import load_dotenv
import json
from SPARQLBurger.SPARQLQueryBuilder import Prefix

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

"""
While the .env and .flaskenv files are similar, Flask expects its own
configuration variables to be in .flaskenv, while application configuration 
variables (including some that can be of a sensitive nature) to be in .env.
"""


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    FUSEKI_URL = os.environ.get("FUSEKI_URL")
    PREFIX_DICT = json.loads(os.environ.get("PREFIX_DICT").replace("'", '"'))
    PREFIX_LIST = [Prefix(prefix, iri) for prefix, iri in PREFIX_DICT.items()]
    ONTOLOGY_IRI = os.environ.get("ONTOLOGY_IRI")
    NAMESPACE_ABR = os.environ.get("NAMESPACE_ABR")
