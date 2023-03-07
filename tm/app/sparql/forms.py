from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, TextAreaField, StringField


class DataCategoryForm(FlaskForm):
    ###################
    # Data Categories #
    ###################

    allergy = BooleanField("Allergy")
    care_plan = BooleanField("Care Plan")
    claim = BooleanField("Claim")
    claim_transaction = BooleanField("Claim Transaction")
    condition = BooleanField("Condition")
    device = BooleanField("Device")
    encounter = BooleanField("Encounter")
    imaging_study = BooleanField("Imaging Study")
    immunization = BooleanField("Immunization")
    medication = BooleanField("Medication")
    observation = BooleanField("Observation")
    organization = BooleanField("Organization")
    patient = BooleanField("Patient")
    payer = BooleanField("Payer")
    payer_transition = BooleanField("Payer Transition")
    procedure = BooleanField("Procedure")
    provider = BooleanField("Provider")
    supply = BooleanField("Supply")

    ######################
    # User Trust Weights #
    ######################

    identity = StringField("Identity Trust", default="0.5")
    behavior = StringField("Behavioral Trust", default="0.5")
    trust_threshold = StringField("Threshold", default="0.5")
    apply_trust_score = BooleanField(
        "USER TRUST SCORE WEIGHTS", default="checked", render_kw={"style": "font-weight: bold;"}
    )

    #########################
    # Data Veracity Weights #
    #########################

    credibility = StringField("Credibility", default="0.3")
    objectivity = StringField("Objectivity", default="0.3")
    trustfulness = StringField("Trustfulness", default="0.4")
    veracity_threshold = StringField("Threshold", default="0.5")
    apply_veracity_score = BooleanField("DATA VERACITY SCORE WEIGHTS", default="checked")

    ############################
    # CONDITION QUERY (SPARQL) #
    ############################

    default_query = 'FILTER (?birthdate > xsd:dateTime("2000-05-23T10:20:13+05:30"))'
    sparql_query = TextAreaField("Condition Query", render_kw={"rows": "11"}, default=default_query)

    ##########
    # LIMITS #
    ##########

    limit = StringField("LIMIT", default=30)

    submit = SubmitField("Submit")


class SPARQLForm(FlaskForm):
    sparql_query = TextAreaField("SPARQL Query", render_kw={"rows": 15})
    submit = SubmitField("Submit")


# - [ ] Add "Apply DUA" Button.


# class PatientDataForm(FlaskForm):
#     address = BooleanField("Address")
#     birthdate = BooleanField("Birth Date", default="checked")
#     birthplace = BooleanField("Birth Place")
#     city = BooleanField("City")
#     county = BooleanField("County")
#     deathdate = BooleanField("Death Date")
#     drivers = BooleanField("Drivers License")
#     ethnicity = BooleanField("Ethnicity")
#     firstname = BooleanField("First Name")
#     gender = BooleanField("Gender")
#     healthcare_coverage = BooleanField("Healthcare Coverage")
#     healthcare_expenses = BooleanField("Healthcare Expenses")
#     id_ = BooleanField("Id")
#     income = BooleanField("Income")
#     lastname = BooleanField("Last Name")
#     marital = BooleanField("Marital Status")
#     passport = BooleanField("Passport Number")
#     race = BooleanField("Race")
#     ssn = BooleanField("SSN")
#     state = BooleanField("State")
#     zip = BooleanField("zip")

#     ###############
#     # Observation #
#     ###############

#     observation_date = BooleanField("Date")
#     observed_patient = BooleanField("Patient")
#     observation_category = BooleanField("Category")
#     observation_code = BooleanField("Code")
#     observation_description = BooleanField("Description")
#     observation_value = BooleanField("Value")
#     observation_units = BooleanField("Units")
#     observation_type = BooleanField("Type")


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
