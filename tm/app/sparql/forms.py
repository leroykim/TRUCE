from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField

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