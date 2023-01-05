import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']

    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE'))

    FUSEKI_URL = "http://localhost:3031/covid19"
    REMOTE_URL_DICT = {
        "http://localhost:3032/covid19":"http://fuseki-2:3030/covid19",
        "http://localhost:3033/covid19":"http://fuseki-3:3030/covid19",
        "http://localhost:3034/covid19":"http://fuseki-4:3030/covid19",
        "http://localhost:3035/covid19":"http://fuseki-5:3030/covid19",
    }
    PREFIX_LIST = ["syn: <https://knacc.umbc.edu/leroy/ontologies/synthea#>",
                    "xsd: <http://www.w3.org/2001/XMLSchema#>"]
    ONTOLOGY_IRI = "https://knacc.umbc.edu/leroy/ontologies/synthea#"
    NAMESPACE_ABR = "syn"
