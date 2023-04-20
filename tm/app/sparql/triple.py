from SPARQLBurger.SPARQLQueryBuilder import SPARQLGraphPattern, Triple

'''
The methods in this file are used to generate variables and data properties of SPARQL queries
for each data category.
'''

def get_variables(data_category_selection: dict) -> list:
    """
    Get variables of selected data categories.
    Methods that returns variables for each data category are defined in the bottom of this file.
    """
    print(f"get_variables: {type(data_category_selection)} {data_category_selection}")
    variable_list = []
    for data_category, isSelected in data_category_selection.items():
        if isSelected:
            variable_list.append(f"?{data_category.lower()}")
            if data_category == "allergy":
                variable_list.extend(get_allergy_variables())
            elif data_category == "care_plan":
                variable_list.extend(get_care_plan_variables())
            elif data_category == "claim":
                variable_list.extend(get_claim_variables())
            elif data_category == "claim_transaction":
                variable_list.extend(get_claim_transaction_variables())
            elif data_category == "condition":
                variable_list.extend(get_condition_variables())
            elif data_category == "device":
                variable_list.extend(get_device_variables())
            elif data_category == "encounter":
                variable_list.extend(get_encounter_variables())
            elif data_category == "imaging_study":
                variable_list.extend(get_imaging_study_variables())
            elif data_category == "immunization":
                variable_list.extend(get_immunization_variables())
            elif data_category == "medication":
                variable_list.extend(get_medication_variables())
            elif data_category == "observation":
                variable_list.extend(get_observation_variables())
            elif data_category == "organization":
                variable_list.extend(get_organization_variables())
            elif data_category == "patient":
                variable_list.extend(get_patient_variables())
            elif data_category == "payer":
                variable_list.extend(get_payer_variables())
            elif data_category == "payer_transition":
                variable_list.extend(get_payer_transition_variables())
            elif data_category == "procedure":
                variable_list.extend(get_procedure_variables())
            elif data_category == "provider":
                variable_list.extend(get_provider_variables())
            elif data_category == "supply":
                variable_list.extend(get_supply_variables())

    return variable_list


def get_data_properties(data_category_selection: dict) -> SPARQLGraphPattern:
    """
    Get data properties of selected data categories.
    Methods that returns data property triples for each data category are defined in the middle of this file.
    Data category list:
    - allergy
    - care_plan
    - claim
    - claim_transaction
    - condition
    - device
    - encounter
    - imaging_study
    - immunization
    - medication
    - observation
    - organization
    - patient
    - payer
    - payer_transiction
    - procedure
    - provider
    - supply
    """
    data_property_pattern = SPARQLGraphPattern()
    for data_category, isSelected in data_category_selection.items():
        if isSelected:
            if data_category == "allergy":
                data_property_pattern.add_triples(get_allergy_data_properties())
            elif data_category == "care_plan":
                data_property_pattern.add_triples(get_care_plan_data_properties())
            elif data_category == "claim":
                data_property_pattern.add_triples(get_claim_data_properties())
            elif data_category == "claim_transaction":
                data_property_pattern.add_triples(get_claim_transaction_data_properties())
            elif data_category == "condition":
                data_property_pattern.add_triples(get_condition_data_properties())
            elif data_category == "device":
                data_property_pattern.add_triples(get_device_data_properties())
            elif data_category == "encounter":
                data_property_pattern.add_triples(get_encounter_data_properties())
            elif data_category == "imaging_study":
                data_property_pattern.add_triples(get_imaging_study_data_properties())
            elif data_category == "immunization":
                data_property_pattern.add_triples(get_immunization_data_properties())
            elif data_category == "medication":
                data_property_pattern.add_triples(get_medication_data_properties())
            elif data_category == "observation":
                data_property_pattern.add_triples(get_observation_data_properties())
            elif data_category == "organization":
                data_property_pattern.add_triples(get_organization_data_properties())
            elif data_category == "patient":
                data_property_pattern.add_triples(get_patient_data_properties())
            elif data_category == "payer":
                data_property_pattern.add_triples(get_payer_data_properties())
            elif data_category == "payer_transition":
                data_property_pattern.add_triples(get_payer_transition_data_properties())
            elif data_category == "procedure":
                data_property_pattern.add_triples(get_procedure_data_properties())
            elif data_category == "provider":
                data_property_pattern.add_triples(get_provider_data_properties())
            elif data_category == "supply":
                data_property_pattern.add_triples(get_supply_data_properties())

    return data_property_pattern


############################
# Specific data properties #
############################


def get_allergy_data_properties() -> list:
    ...


def get_care_plan_data_properties() -> list:
    ...


def get_claim_data_properties() -> list:
    ...


def get_claim_transaction_data_properties() -> list:
    ...


def get_condition_data_properties() -> list:
    ...


def get_device_data_properties() -> list:
    ...


def get_encounter_data_properties() -> list:
    ...


def get_imaging_study_data_properties() -> list:
    ...


def get_immunization_data_properties() -> list:
    ...


def get_medication_data_properties() -> list:
    ...


def get_observation_data_properties() -> list:
    ...


def get_organization_data_properties() -> list:
    ...


def get_patient_data_properties() -> list:
    """
    Get data properties of Patient class.
    Data property list:
    - id
    - birthdate
    - ssn
    - first
    - last
    - race
    - ethnicity
    - gender
    - birthplace
    - address
    - city
    - state
    - healthcareExpense
    - healthcareCoverage
    - income
    """
    triples = [
        Triple(subject="?patient", predicate="syn:id", object="?patient_id"),
        Triple(subject="?patient", predicate="syn:birthdate", object="?patient_birthdate"),
        Triple(subject="?patient", predicate="syn:ssn", object="?patient_ssn"),
        Triple(subject="?patient", predicate="syn:first", object="?patient_first"),
        Triple(subject="?patient", predicate="syn:last", object="?patient_last"),
        Triple(subject="?patient", predicate="syn:race", object="?patient_race"),
        Triple(subject="?patient", predicate="syn:ethnicity", object="?patient_ethnicity"),
        Triple(subject="?patient", predicate="syn:gender", object="?patient_gender"),
        Triple(subject="?patient", predicate="syn:birthplace", object="?patient_birthplace"),
        Triple(subject="?patient", predicate="syn:address", object="?patient_address"),
        Triple(subject="?patient", predicate="syn:city", object="?patient_city"),
        Triple(subject="?patient", predicate="syn:state", object="?patient_state"),
        Triple(subject="?patient", predicate="syn:healthcareExpense", object="?patient_healthcareExpense"),
        Triple(subject="?patient", predicate="syn:healthcareCoverage", object="?patient_healthcareCoverage"),
        Triple(subject="?patient", predicate="syn:income", object="?patient_income"),
    ]
    return triples


def get_payer_data_properties() -> list:
    ...


def get_payer_transition_data_properties() -> list:
    ...


def get_procedure_data_properties() -> list:
    ...


def get_provider_data_properties() -> list:
    ...


def get_supply_data_properties() -> list:
    ...


####################################
# Variables for each data category #
####################################


def get_allergy_variables() -> list:
    ...


def get_care_plan_variables() -> list:
    ...


def get_claim_variables() -> list:
    ...


def get_claim_transaction_variables() -> list:
    ...


def get_condition_variables() -> list:
    ...


def get_device_variables() -> list:
    ...


def get_encounter_variables() -> list:
    ...


def get_imaging_study_variables() -> list:
    ...


def get_immunization_variables() -> list:
    ...


def get_medication_variables() -> list:
    ...


def get_observation_variables() -> list:
    ...


def get_organization_variables() -> list:
    ...


def get_patient_variables() -> list:
    """
    Get variables of Patient class.
    """
    variables = [
        "?patient_id",
        "?patient_birthdate",
        "?patient_ssn",
        "?patient_first",
        "?patient_last",
        "?patient_race",
        "?patient_ethnicity",
        "?patient_gender",
        "?patient_birthplace",
        "?patient_address",
        "?patient_city",
        "?patient_state",
        "?patient_healthcareExpense",
        "?patient_healthcareCoverage",
        "?patient_income",
    ]
    return variables


def get_payer_variables() -> list:
    ...


def get_payer_transition_variables() -> list:
    ...


def get_procedure_variables() -> list:
    ...


def get_provider_variables() -> list:
    ...


def get_supply_variables() -> list:
    ...
