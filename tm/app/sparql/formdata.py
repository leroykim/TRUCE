from app.sparql.forms import PatientDataForm

def get_patient_variables(form: PatientDataForm) -> dict:
    patient_selection_dict = {}
    patient_selection_dict["address"] = form.address.data
    patient_selection_dict["birthdate"] = form.birthdate.data
    patient_selection_dict["birthplace"] = form.birthplace.data
    patient_selection_dict["city"] = form.city.data
    patient_selection_dict["county"] = form.county.data
    patient_selection_dict["deathdate"] = form.deathdate.data
    patient_selection_dict["drivers"] = form.drivers.data
    patient_selection_dict["ethnicity"] = form.ethnicity.data
    patient_selection_dict["firstname"] = form.firstname.data
    patient_selection_dict["gender"] = form.gender.data
    patient_selection_dict["healthcare_coverage"] = (
        form.healthcare_coverage.data)
    patient_selection_dict["healthcare_expenses"] = (
        form.healthcare_expenses.data)
    patient_selection_dict["id_"] = form.id_.data
    patient_selection_dict["income"] = form.income.data
    patient_selection_dict["lastname"] = form.lastname.data
    patient_selection_dict["marital"] = form.marital.data
    patient_selection_dict["passport"] = form.passport.data
    patient_selection_dict["race"] = form.race.data
    patient_selection_dict["ssn"] = form.ssn.data
    patient_selection_dict["state"] = form.state.data
    patient_selection_dict["zip"] = form.zip.data

    return patient_selection_dict

def get_score_weights(form: PatientDataForm) -> dict:
    score_weights = {}
    score_weights["identity"] = float(form.identity.data)
    score_weights["behavior"] = float(form.behavior.data)
    score_weights["credibility"] = float(form.credibility.data)
    score_weights["objectivity"] = float(form.objectivity.data)
    score_weights["trustfulness"] = float(form.trustfulness.data)
    score_weights["trust_threshold"] = float(form.trust_threshold.data)
    score_weights["veracity_threshold"] = float(form.veracity_threshold.data)

    return score_weights
