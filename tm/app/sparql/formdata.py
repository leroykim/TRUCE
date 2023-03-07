from app.sparql.forms import PatientDataForm, DataCategoryForm


def get_data_category(form: DataCategoryForm) -> dict:
    data_category = {}
    data_category["allergy"] = form.allergy.data
    data_category["care_plan"] = form.care_plan.data
    data_category["claim"] = form.claim.data
    data_category["claim_transaction"] = form.claim_transaction.data
    data_category["condition"] = form.condition.data
    data_category["device"] = form.device.data
    data_category["encounter"] = form.encounter.data
    data_category["imaging_study"] = form.imaging_study.data
    data_category["immunization"] = form.immunization.data
    data_category["medication"] = form.medication.data
    data_category["observation"] = form.observation.data
    data_category["organization"] = form.organization.data
    data_category["patient"] = form.patient.data
    data_category["payer"] = form.payer.data
    data_category["payer_transiction"] = form.payer_transition.data
    data_category["procedure"] = form.procedure.data
    data_category["provider"] = form.provider.data
    data_category["supply"] = form.supply.data

    return data_category


def get_score_weights(form: PatientDataForm) -> dict:
    score_weights = {}
    score_weights["identity"] = float(form.identity.data)
    score_weights["behavior"] = float(form.behavior.data)
    score_weights["credibility"] = float(form.credibility.data)
    score_weights["objectivity"] = float(form.objectivity.data)
    score_weights["trustfulness"] = float(form.trustfulness.data)

    score_weights["trust_threshold"] = float(form.trust_threshold.data)
    score_weights["veracity_threshold"] = float(form.veracity_threshold.data)

    score_weights["apply_trust_score"] = bool(form.apply_trust_score.data)
    score_weights["apply_veracity_score"] = bool(form.apply_veracity_score.data)

    return score_weights


def get_limit(form: PatientDataForm) -> int:
    return int(form.limit.data)


# def get_patient_selections(form: PatientDataForm) -> dict:
#     patient_selections = {}
#     patient_selections["address"] = form.address.data
#     patient_selections["birthdate"] = form.birthdate.data
#     patient_selections["birthplace"] = form.birthplace.data
#     patient_selections["city"] = form.city.data
#     patient_selections["county"] = form.county.data
#     patient_selections["deathdate"] = form.deathdate.data
#     patient_selections["drivers"] = form.drivers.data
#     patient_selections["ethnicity"] = form.ethnicity.data
#     patient_selections["firstname"] = form.firstname.data
#     patient_selections["gender"] = form.gender.data
#     patient_selections["healthcare_coverage"] = form.healthcare_coverage.data
#     patient_selections["healthcare_expenses"] = form.healthcare_expenses.data
#     patient_selections["id_"] = form.id_.data
#     patient_selections["income"] = form.income.data
#     patient_selections["lastname"] = form.lastname.data
#     patient_selections["marital"] = form.marital.data
#     patient_selections["passport"] = form.passport.data
#     patient_selections["race"] = form.race.data
#     patient_selections["ssn"] = form.ssn.data
#     patient_selections["state"] = form.state.data
#     patient_selections["zip"] = form.zip.data

#     return patient_selections


# def get_observation_selections(form: PatientDataForm) -> dict:
#     observation_selections = {}
#     observation_selections["date"] = form.observation_date.data
#     observation_selections["observedPatient"] = form.observed_patient.data
#     observation_selections["category"] = form.observation_category.data
#     observation_selections["observation_code"] = form.observation_code.data
#     observation_selections["observation_description"] = form.observation_description.data
#     observation_selections["value"] = form.observation_value.data
#     observation_selections["units"] = form.observation_units.data
#     observation_selections["type"] = form.observation_type.data

#     return observation_selections
