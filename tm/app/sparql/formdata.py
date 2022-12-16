from app.sparql.forms import PatientDataForm

def get_patient_selection(form: PatientDataForm):
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