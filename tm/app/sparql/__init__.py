from flask import Blueprint

bp = Blueprint('sparql', __name__)

from app.sparql import routes