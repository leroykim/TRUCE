from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, TextAreaField, StringField


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
    sparql_query = TextAreaField("SPARQL Query", render_kw={"rows": 15})
    submit = SubmitField('Submit')


class PatientDataForm(FlaskForm):
    address = BooleanField('Address')
    birthdate = BooleanField('Birth Date')
    birthplace = BooleanField('Birth Place')
    city = BooleanField('City')
    county = BooleanField('County')
    deathdate = BooleanField('Death Date')
    drivers = BooleanField('Drivers License')
    ethnicity = BooleanField('Ethnicity')
    firstname = BooleanField('First Name')
    gender = BooleanField('Gender')
    healthcare_coverage = BooleanField('Healthcare Coverage')
    healthcare_expenses = BooleanField('Healthcare Expenses')
    id_ = BooleanField('Id')
    income = BooleanField('Income')
    lastname = BooleanField('Last Name')
    marital = BooleanField('Marital Status')
    passport = BooleanField('Passport Number')
    race = BooleanField('Race')
    ssn = BooleanField('SSN')
    state = BooleanField('State')
    zip = BooleanField('zip')

    sparql_query = TextAreaField("SPARQL Query", render_kw={"rows": 11})

    # User trust Score
    identity = StringField('Identity Trust', default="0.5")
    behavior = StringField('Behavioral Trust', default="0.5")
    trust_threshold = StringField('Threshold', default="0.5")
    #Veracity
    credibility = StringField('Credibility', default="0.3")
    objectivity = StringField('Objectivity',default="0.3")
    trustfulness = StringField('Trustfulness', default="0.4")
    veracity_threshold = StringField('Threshold', default="0.5")

    submit = SubmitField('Submit')

# class SettingForm(FlaskForm):
#     # User trust Score
#     identity = StringField('Identity Trust')
#     behavior = StringField('Behavioral Trust')
#     trust_threshold = StringField('Threshold')
#     #Veracity
#     credibility = StringField('Credibility')
#     objectivity = StringField('Objectivity')
#     trustfulness = StringField('Trustfulness')
#     veracity_threshold = StringField('Threshold')
    
#     submit = SubmitField('Save')