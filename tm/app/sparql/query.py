from app.sparql.forms import PatientDataForm


def get_patient_select_clause(form_data: PatientDataForm):
    variable_list = get_patient_variable_list(form_data)
    sparql_variable_list = ["?" + i for i in variable_list]
    select_clause = "SELECT " + ', '.join(sparql_variable_list) + '\n'
    return select_clause


def get_patient_variable_list(form_data: PatientDataForm):
    patient_selection_dict = get_patient_selection_dict(form_data)
    variable_list = []
    for key, value in patient_selection_dict.items():
        if value:
            variable_list.append(key)
    return variable_list


def get_patient_selection_dict(form_data: PatientDataForm):
    patient_selection_dict = {}
    patient_selection_dict["address"] = form_data.address.data
    patient_selection_dict["birthdate"] = form_data.birthdate.data
    patient_selection_dict["birthplace"] = form_data.birthplace.data
    patient_selection_dict["city"] = form_data.city.data
    patient_selection_dict["county"] = form_data.county.data
    patient_selection_dict["deathdate"] = form_data.deathdate.data
    patient_selection_dict["drivers"] = form_data.drivers.data
    patient_selection_dict["ethnicity"] = form_data.ethnicity.data
    patient_selection_dict["firstname"] = form_data.firstname.data
    patient_selection_dict["gender"] = form_data.gender.data
    patient_selection_dict["healthcare_coverage"] = (
        form_data.healthcare_coverage.data)
    patient_selection_dict["healthcare_expenses"] = (
        form_data.healthcare_expenses.data)
    patient_selection_dict["id_"] = form_data.id_.data
    patient_selection_dict["income"] = form_data.income.data
    patient_selection_dict["lastname"] = form_data.lastname.data
    patient_selection_dict["marital"] = form_data.marital.data
    patient_selection_dict["passport"] = form_data.passport.data
    patient_selection_dict["race"] = form_data.race.data
    patient_selection_dict["ssn"] = form_data.ssn.data
    patient_selection_dict["state"] = form_data.state.data
    patient_selection_dict["zip"] = form_data.zip.data

    return patient_selection_dict


def get_where_clause(form_data: PatientDataForm):
    sparql_query = form_data.sparql_query.data
    variable_list = get_patient_variable_list(form_data)
    variable_triple_list = [f"?patient syn:{i} ?{i} ." for i in variable_list]
    variable_triple_string = '\n'.join(variable_triple_list)
    where_clause = '\n'.join([
        "WHERE {",
        "?patient a syn:Patient .",
        variable_triple_string,
        sparql_query,
        "}"
    ])
    return where_clause


def get_policy():
    ...
