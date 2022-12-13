from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    current_app
from flask_login import current_user, login_required
from app.sparql import bp

@bp.route('/query')
def query():
    return render_template('sparql/query.html', title='SPARQL')