from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, TextAreaField

class DataForm(FlaskForm):
    CATEGORIES = [
            ('patient', 'Patient'), 
            ('encounter', 'Encounter'), 
            ('observation', 'Observation')
            ]
    FIELDS = [('name', 'Name'), ('age', 'Age')]
    category = SelectField('Data Category', choices=CATEGORIES)
    name = BooleanField('Name')
    age = BooleanField('Age')
    submit = SubmitField('Submit')

class SPARQLForm(FlaskForm):
    sparql_query = TextAreaField("SPARQL Query", render_kw={"rows":30})
    submit = SubmitField('Submit')