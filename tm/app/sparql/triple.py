from SPARQLBurger.SPARQLQueryBuilder import SPARQLGraphPattern, Triple
from flask import current_app

"""
The methods in this file are used to generate variables and data properties of SPARQL queries
for each data category.
"""


def get_variables(data_category_selection: dict) -> list:
    """
    Get variables of selected data categories.
    Methods that returns variables for each data category are defined in the bottom of this file.
    """
    # current_app.logger.info(
    #     f"get_variables: {type(data_category_selection)} {data_category_selection}"
    # )
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
        data_category = data_category.lower()
        if isSelected:
            if data_category == "allergy":
                data_property_pattern.add_triples(get_allergy_data_properties())
            elif data_category == "care_plan":
                data_property_pattern.add_triples(get_care_plan_data_properties())
            elif data_category == "claim":
                data_property_pattern.add_triples(get_claim_data_properties())
            elif data_category == "claim_transaction":
                data_property_pattern.add_triples(
                    get_claim_transaction_data_properties()
                )
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
                data_property_pattern.add_triples(
                    get_payer_transition_data_properties()
                )
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
    """
    Get data properties of CarePlan class.
    Data property list:
    - code
    - description
    - encounterId
    - id
    - patientId
    - reasonCode
    - reasonDescription
    - startDate
    """
    triples = [
        Triple(
            subject="?care_plan",
            predicate="syn:code",
            object="?care_plan_code",
        ),
        Triple(
            subject="?care_plan",
            predicate="syn:description",
            object="?care_plan_description",
        ),
        Triple(
            subject="?care_plan",
            predicate="syn:encounterId",
            object="?care_plan_encounterId",
        ),
        Triple(
            subject="?care_plan",
            predicate="syn:id",
            object="?care_plan_id",
        ),
        Triple(
            subject="?care_plan",
            predicate="syn:patientId",
            object="?care_plan_patientId",
        ),
        Triple(
            subject="?care_plan",
            predicate="syn:reasonCode",
            object="?care_plan_reasonCode",
        ),
        Triple(
            subject="?care_plan",
            predicate="syn:reasonDescription",
            object="?care_plan_reasonDescription",
        ),
        Triple(
            subject="?care_plan",
            predicate="syn:startDate",
            object="?care_plan_startDate",
        ),
    ]

    return triples


def get_claim_data_properties() -> list:
    """
    Get data properties of Claim class.
    Data property list:
    - currentIllnessDate
    - departmentId
    - id
    - patientDepartmentId
    - patientId
    - providerId
    - serviceDate
    """
    triples = [
        Triple(
            subject="?claim",
            predicate="syn:currentIllnessDate",
            object="?claim_currentIllnessDate",
        ),
        Triple(
            subject="?claim",
            predicate="syn:departmentId",
            object="?claim_departmentId",
        ),
        Triple(
            subject="?claim",
            predicate="syn:id",
            object="?claim_id",
        ),
        Triple(
            subject="?claim",
            predicate="syn:patientDepartmentId",
            object="?claim_patientDepartmentId",
        ),
        Triple(
            subject="?claim",
            predicate="syn:patientId",
            object="?claim_patientId",
        ),
        Triple(
            subject="?claim",
            predicate="syn:providerId",
            object="?claim_providerId",
        ),
        Triple(
            subject="?claim",
            predicate="syn:serviceDate",
            object="?claim_serviceDate",
        ),
    ]

    return triples


def get_claim_transaction_data_properties() -> list:
    """
    Get data properties of ClaimTransaction class.
    Data property list:
    - chargeId
    - claimId
    - claimTransactionType
    - id
    - placeOfService
    - procedureCode
    - providerId
    """
    triples = [
        Triple(
            subject="?claim_transaction",
            predicate="syn:chargeId",
            object="?claim_transaction_chargeId",
        ),
        Triple(
            subject="?claim_transaction",
            predicate="syn:claimId",
            object="?claim_transaction_claimId",
        ),
        Triple(
            subject="?claim_transaction",
            predicate="syn:claimTransactionType",
            object="?claim_transaction_claimTransactionType",
        ),
        Triple(
            subject="?claim_transaction",
            predicate="syn:id",
            object="?claim_transaction_id",
        ),
        Triple(
            subject="?claim_transaction",
            predicate="syn:placeOfService",
            object="?claim_transaction_placeOfService",
        ),
        Triple(
            subject="?claim_transaction",
            predicate="syn:procedureCode",
            object="?claim_transaction_procedureCode",
        ),
        Triple(
            subject="?claim_transaction",
            predicate="syn:providerId",
            object="?claim_transaction_providerId",
        ),
    ]

    return triples


def get_condition_data_properties() -> list:
    """
    Get data properties of Condition class.
    Data property list:
    - code
    - description
    - encounterId
    - patientId
    - startDate
    """
    triples = [
        Triple(
            subject="?condition",
            predicate="syn:code",
            object="?condition_code",
        ),
        Triple(
            subject="?condition",
            predicate="syn:description",
            object="?condition_description",
        ),
        Triple(
            subject="?condition",
            predicate="syn:encounterId",
            object="?condition_encounterId",
        ),
        Triple(
            subject="?condition",
            predicate="syn:patientId",
            object="?condition_patientId",
        ),
        Triple(
            subject="?condition",
            predicate="syn:startDate",
            object="?condition_startDate",
        ),
    ]

    return triples


def get_device_data_properties() -> list:
    """
    Get data properties of Device class.
    Data property list:
    - code
    - description
    - encounterId
    - patientId
    - startDateTime
    - udi
    """
    triples = [
        Triple(
            subject="?device",
            predicate="syn:code",
            object="?device_code",
        ),
        Triple(
            subject="?device",
            predicate="syn:description",
            object="?device_description",
        ),
        Triple(
            subject="?device",
            predicate="syn:encounterId",
            object="?device_encounterId",
        ),
        Triple(
            subject="?device",
            predicate="syn:patientId",
            object="?device_patientId",
        ),
        Triple(
            subject="?device",
            predicate="syn:startDateTime",
            object="?device_startDateTime",
        ),
        Triple(
            subject="?device",
            predicate="syn:udi",
            object="?device_udi",
        ),
    ]

    return triples


def get_encounter_data_properties() -> list:
    """
    Get data properties of Encounter class.
    Data property list:
    - baseEncounterCost
    - code
    - description
    - encounterClass
    - id
    - organizationId
    - patientId
    - payerCoverage
    - payerId
    - providerId
    - startDateTime
    - totalClaimCost
    """
    triples = [
        Triple(
            subject="?encounter",
            predicate="syn:baseEncounterCost",
            object="?encounter_baseEncounterCost",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:code",
            object="?encounter_code",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:description",
            object="?encounter_description",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:encounterClass",
            object="?encounter_encounterClass",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:id",
            object="?encounter_id",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:organizationId",
            object="?encounter_organizationId",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:patientId",
            object="?encounter_patientId",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:payerCoverage",
            object="?encounter_payerCoverage",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:payerId",
            object="?encounter_payerId",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:providerId",
            object="?encounter_providerId",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:startDateTime",
            object="?encounter_startDateTime",
        ),
        Triple(
            subject="?encounter",
            predicate="syn:totalClaimCost",
            object="?encounter_totalClaimCost",
        ),
    ]

    return triples


def get_imaging_study_data_properties() -> list:
    ...


def get_immunization_data_properties() -> list:
    """
    Get data properties of Immunization class.
    Data property list:
    - code
    - cost
    - dateTime
    - description
    - encounterId
    - patientId
    """
    triples = [
        Triple(
            subject="?immunization",
            predicate="syn:code",
            object="?immunization_code",
        ),
        Triple(
            subject="?immunization",
            predicate="syn:cost",
            object="?immunization_cost",
        ),
        Triple(
            subject="?immunization",
            predicate="syn:dateTime",
            object="?immunization_dateTime",
        ),
        Triple(
            subject="?immunization",
            predicate="syn:description",
            object="?immunization_description",
        ),
        Triple(
            subject="?immunization",
            predicate="syn:encounterId",
            object="?immunization_encounterId",
        ),
        Triple(
            subject="?immunization",
            predicate="syn:patientId",
            object="?immunization_patientId",
        ),
    ]

    return triples


def get_medication_data_properties() -> list:
    """
    Get data properties of Medication class.
    Data property list:
    - baseCost
    - code
    - description
    - dispense
    - encounterId
    - patientId
    - payerCoverage
    - payerId
    - startDateTime
    - totalCost
    """
    triples = [
        Triple(
            subject="?medication",
            predicate="syn:baseCost",
            object="?medication_baseCost",
        ),
        Triple(
            subject="?medication",
            predicate="syn:code",
            object="?medication_code",
        ),
        Triple(
            subject="?medication",
            predicate="syn:description",
            object="?medication_description",
        ),
        Triple(
            subject="?medication",
            predicate="syn:dispense",
            object="?medication_dispense",
        ),
        Triple(
            subject="?medication",
            predicate="syn:encounterId",
            object="?medication_encounterId",
        ),
        Triple(
            subject="?medication",
            predicate="syn:patientId",
            object="?medication_patientId",
        ),
        Triple(
            subject="?medication",
            predicate="syn:payerCoverage",
            object="?medication_payerCoverage",
        ),
        Triple(
            subject="?medication",
            predicate="syn:payerId",
            object="?medication_payerId",
        ),
        Triple(
            subject="?medication",
            predicate="syn:startDateTime",
            object="?medication_startDateTime",
        ),
        Triple(
            subject="?medication",
            predicate="syn:totalCost",
            object="?medication_totalCost",
        ),
    ]

    return triples


def get_observation_data_properties() -> list:
    """
    Get data properties of Observation class.
    Data property list:
    - code
    - dateTime
    - description
    - encounterId
    - patientId
    - type
    - value
    """
    triples = [
        Triple(
            subject="?observation",
            predicate="syn:code",
            object="?observation_code",
        ),
        Triple(
            subject="?observation",
            predicate="syn:dateTime",
            object="?observation_dateTime",
        ),
        Triple(
            subject="?observation",
            predicate="syn:description",
            object="?observation_description",
        ),
        Triple(
            subject="?observation",
            predicate="syn:encounterId",
            object="?observation_encounterId",
        ),
        Triple(
            subject="?observation",
            predicate="syn:patientId",
            object="?observation_patientId",
        ),
        Triple(
            subject="?observation",
            predicate="syn:type",
            object="?observation_type",
        ),
        Triple(
            subject="?observation",
            predicate="syn:value",
            object="?observation_value",
        ),
    ]

    return triples


def get_organization_data_properties() -> list:
    """
    Get data properties of Organization class.
    Data property list:
    - address
    - city
    - id
    - name
    - revenue
    - utilization
    """
    triples = [
        Triple(
            subject="?organization",
            predicate="syn:address",
            object="?organization_address",
        ),
        Triple(
            subject="?organization",
            predicate="syn:city",
            object="?organization_city",
        ),
        Triple(
            subject="?organization",
            predicate="syn:id",
            object="?organization_id",
        ),
        Triple(
            subject="?organization",
            predicate="syn:name",
            object="?organization_name",
        ),
        Triple(
            subject="?organization",
            predicate="syn:revenue",
            object="?organization_revenue",
        ),
        Triple(
            subject="?organization",
            predicate="syn:utilization",
            object="?organization_utilization",
        ),
    ]

    return triples


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
        Triple(
            subject="?patient", predicate="syn:birthdate", object="?patient_birthdate"
        ),
        Triple(subject="?patient", predicate="syn:ssn", object="?patient_ssn"),
        Triple(subject="?patient", predicate="syn:first", object="?patient_first"),
        Triple(subject="?patient", predicate="syn:last", object="?patient_last"),
        Triple(subject="?patient", predicate="syn:race", object="?patient_race"),
        Triple(
            subject="?patient", predicate="syn:ethnicity", object="?patient_ethnicity"
        ),
        Triple(subject="?patient", predicate="syn:gender", object="?patient_gender"),
        Triple(
            subject="?patient", predicate="syn:birthplace", object="?patient_birthplace"
        ),
        Triple(subject="?patient", predicate="syn:address", object="?patient_address"),
        Triple(subject="?patient", predicate="syn:city", object="?patient_city"),
        Triple(subject="?patient", predicate="syn:state", object="?patient_state"),
        Triple(
            subject="?patient",
            predicate="syn:healthcareExpense",
            object="?patient_healthcareExpense",
        ),
        Triple(
            subject="?patient",
            predicate="syn:healthcareCoverage",
            object="?patient_healthcareCoverage",
        ),
        Triple(subject="?patient", predicate="syn:income", object="?patient_income"),
    ]
    return triples


def get_payer_data_properties() -> list:
    """
    Get data properties of Payer class.
    Data property list:
    - amountCovered
    - amountUncovered
    - coveredEncounters
    - coveredImmunizations
    - coveredMedications
    - coveredProcedures
    - id
    - memberMonths
    - name
    - qolsAvg
    - revenue
    - uncoveredEncounters
    - uncoveredImmunizations
    - uncoveredMedications
    - uncoveredProcedures
    - uniqueCustomers
    """
    triples = [
        Triple(
            subject="?payer",
            predicate="syn:amountCovered",
            object="?payer_amountCovered",
        ),
        Triple(
            subject="?payer",
            predicate="syn:amountUncovered",
            object="?payer_amountUncovered",
        ),
        Triple(
            subject="?payer",
            predicate="syn:coveredEncounters",
            object="?payer_coveredEncounters",
        ),
        Triple(
            subject="?payer",
            predicate="syn:coveredImmunizations",
            object="?payer_coveredImmunizations",
        ),
        Triple(
            subject="?payer",
            predicate="syn:coveredMedications",
            object="?payer_coveredMedications",
        ),
        Triple(
            subject="?payer",
            predicate="syn:coveredProcedures",
            object="?payer_coveredProcedures",
        ),
        Triple(subject="?payer", predicate="syn:id", object="?payer_id"),
        Triple(
            subject="?payer",
            predicate="syn:memberMonths",
            object="?payer_memberMonths",
        ),
        Triple(subject="?payer", predicate="syn:name", object="?payer_name"),
        Triple(subject="?payer", predicate="syn:qolsAvg", object="?payer_qolsAvg"),
        Triple(subject="?payer", predicate="syn:revenue", object="?payer_revenue"),
        Triple(
            subject="?payer",
            predicate="syn:uncoveredEncounters",
            object="?payer_uncoveredEncounters",
        ),
        Triple(
            subject="?payer",
            predicate="syn:uncoveredImmunizations",
            object="?payer_uncoveredImmunizations",
        ),
        Triple(
            subject="?payer",
            predicate="syn:uncoveredMedications",
            object="?payer_uncoveredMedications",
        ),
        Triple(
            subject="?payer",
            predicate="syn:uncoveredProcedures",
            object="?payer_uncoveredProcedures",
        ),
        Triple(
            subject="?payer",
            predicate="syn:uniqueCustomers",
            object="?payer_uniqueCustomers",
        ),
    ]
    return triples


def get_payer_transition_data_properties() -> list:
    """
    Get data properties of PayerTransition class.
    Data property list:
    - endYear
    - patientId
    - payerId
    - startYear
    """
    triples = [
        Triple(
            subject="?payerTransition",
            predicate="syn:endYear",
            object="?payerTransition_endYear",
        ),
        Triple(
            subject="?payerTransition",
            predicate="syn:patientId",
            object="?payerTransition_patientId",
        ),
        Triple(
            subject="?payerTransition",
            predicate="syn:payerId",
            object="?payerTransition_payerId",
        ),
        Triple(
            subject="?payerTransition",
            predicate="syn:startYear",
            object="?payerTransition_startYear",
        ),
    ]
    return triples


def get_procedure_data_properties() -> list:
    """
    Get data properties of Procedure class.
    Data property list:
    - baseCost
    - code
    - description
    - encounterId
    - patientId
    - startDateTime
    """
    triples = [
        Triple(
            subject="?procedure",
            predicate="syn:baseCost",
            object="?procedure_baseCost",
        ),
        Triple(subject="?procedure", predicate="syn:code", object="?procedure_code"),
        Triple(
            subject="?procedure",
            predicate="syn:description",
            object="?procedure_description",
        ),
        Triple(
            subject="?procedure",
            predicate="syn:encounterId",
            object="?procedure_encounterId",
        ),
        Triple(
            subject="?procedure",
            predicate="syn:patientId",
            object="?procedure_patientId",
        ),
        Triple(
            subject="?procedure",
            predicate="syn:startDateTime",
            object="?procedure_startDateTime",
        ),
    ]
    return triples


def get_provider_data_properties() -> list:
    """
    Get data properties of Provider class.
    Data property list:
    - address
    - city
    - gender
    - id
    - name
    - organizationId
    - specialty
    - utilization
    """
    triples = [
        Triple(
            subject="?provider",
            predicate="syn:address",
            object="?provider_address",
        ),
        Triple(subject="?provider", predicate="syn:city", object="?provider_city"),
        Triple(
            subject="?provider",
            predicate="syn:gender",
            object="?provider_gender",
        ),
        Triple(subject="?provider", predicate="syn:id", object="?provider_id"),
        Triple(subject="?provider", predicate="syn:name", object="?provider_name"),
        Triple(
            subject="?provider",
            predicate="syn:organizationId",
            object="?provider_organizationId",
        ),
        Triple(
            subject="?provider",
            predicate="syn:specialty",
            object="?provider_specialty",
        ),
        Triple(
            subject="?provider",
            predicate="syn:utilization",
            object="?provider_utilization",
        ),
    ]
    return triples


def get_supply_data_properties() -> list:
    """
    Get data properties of Supply class.
    Data property list:
    - code
    - date
    - description
    - encounterId
    - patientId
    - quantity
    """
    triples = [
        Triple(subject="?supply", predicate="syn:code", object="?supply_code"),
        Triple(subject="?supply", predicate="syn:date", object="?supply_date"),
        Triple(
            subject="?supply",
            predicate="syn:description",
            object="?supply_description",
        ),
        Triple(
            subject="?supply",
            predicate="syn:encounterId",
            object="?supply_encounterId",
        ),
        Triple(
            subject="?supply",
            predicate="syn:patientId",
            object="?supply_patientId",
        ),
        Triple(
            subject="?supply",
            predicate="syn:quantity",
            object="?supply_quantity",
        ),
    ]
    return triples


####################################
# Variables for each data category #
####################################


def get_allergy_variables() -> list:
    ...


def get_care_plan_variables() -> list:
    """
    Get variables of CarePlan class.
    """
    variables = [
        "?care_plan_code",
        "?care_plan_description",
        "?care_plan_encounterId",
        "?care_plan_id",
        "?care_plan_patientId",
        "?care_plan_reasonCode",
        "?care_plan_reasonDescription",
        "?care_plan_startDate",
    ]

    return variables


def get_claim_variables() -> list:
    """
    Get variables of Claim class.
    """
    variables = [
        "?claim_currentIllnessDate",
        "?claim_departmentId",
        "?claim_id",
        "?claim_patientDepartmentId",
        "?claim_patientId",
        "?claim_providerId",
        "?claim_serviceDate",
    ]

    return variables


def get_claim_transaction_variables() -> list:
    """
    Get variables of ClaimTransaction class.
    """
    variables = [
        "?claim_transaction_chargeId",
        "?claim_transaction_claimId",
        "?claim_transaction_claimTransactionType",
        "?claim_transaction_id",
        "?claim_transaction_patientId",
        "?claim_transaction_placeOfService",
        "?claim_transaction_procedureCode",
        "?claim_transaction_providerId",
    ]

    return variables


def get_condition_variables() -> list:
    """
    Get variables of Condition class.
    """
    variables = [
        "?condition_code",
        "?condition_description",
        "?condition_encounterId",
        "?condition_patientId",
        "?condition_startDate",
    ]

    return variables


def get_device_variables() -> list:
    """
    Get variables of Device class.
    """
    variables = [
        "?device_code",
        "?device_description",
        "?device_encounterId",
        "?device_patientId",
        "?device_startDateTime",
        "?device_udi",
    ]

    return variables


def get_encounter_variables() -> list:
    """
    Get variables of Encounter class.
    """
    variables = [
        "?encounter_baseEncounterCost",
        "?encounter_code",
        "?encounter_description",
        "?encounter_encounterClass",
        "?encounter_id",
        "?encounter_organizationId",
        "?encounter_patientId",
        "?encounter_payerCoverage",
        "?encounter_payerId",
        "?encounter_providerId",
        "?encounter_startDateTime",
        "?encounter_totalClaimCost",
    ]

    return variables


def get_imaging_study_variables() -> list:
    ...


def get_immunization_variables() -> list:
    """
    Get variables of Immunization class.
    """
    variables = [
        "?immunization_code",
        "?immunization_cost",
        "?immunization_dateTime",
        "?immunization_description",
        "?immunization_encounterId",
        "?immunization_patientId",
    ]

    return variables


def get_medication_variables() -> list:
    """
    Get variables of Medication class.
    """
    variables = [
        "?medication_baseCost",
        "?medication_code",
        "?medication_description",
        "?medication_dispense",
        "?medication_encounterId",
        "?medication_patientId",
        "?medication_payerCoverage",
        "?medication_payerId",
        "?medication_startDateTime",
        "?medication_totalCost",
    ]

    return variables


def get_observation_variables() -> list:
    """
    Get variables of Observation class.
    """
    variables = [
        "?observation_code",
        "?observation_dateTime",
        "?observation_description",
        "?observation_encounterId",
        "?observation_patientId",
        "?observation_type",
        "?observation_value",
    ]

    return variables


def get_organization_variables() -> list:
    """
    Get variables of Organization class.
    """
    variables = [
        "?organization_address",
        "?organization_city",
        "?organization_id",
        "?organization_name",
        "?organization_revenue",
        "?organization_utilization",
    ]

    return variables


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
    """
    Get variables of Payer class.
    """
    variables = [
        "?payer_amountCovered",
        "?payer_amountUncovered",
        "?payer_coveredEncounters",
        "?payer_coveredImmunizations",
        "?payer_coveredMedications",
        "?payer_coveredProcedures",
        "?payer_id",
        "?payer_memberMonths",
        "?payer_name",
        "?payer_qolsAvg",
        "?payer_revenue",
        "?payer_uncoveredEncounters",
        "?payer_uncoveredImmunizations",
        "?payer_uncoveredMedications",
        "?payer_uncoveredProcedures",
        "?payer_uniqueCustomers",
    ]

    return variables


def get_payer_transition_variables() -> list:
    """
    Get variables of PayerTransition class.
    """
    variables = [
        "?payer_transition_endYear",
        "?payer_transition_patientId",
        "?payer_transition_payerId",
        "?payer_transition_startYear",
    ]

    return variables


def get_procedure_variables() -> list:
    """
    Get variables of Procedure class.
    """
    variables = [
        "?procedure_baseCost",
        "?procedure_code",
        "?procedure_description",
        "?procedure_encounterId",
        "?procedure_patientId",
        "?procedure_startDateTime",
    ]

    return variables


def get_provider_variables() -> list:
    """
    Get variables of Provider class.
    """
    variables = [
        "?provider_address",
        "?provider_city",
        "?provider_gender",
        "?provider_id",
        "?provider_name",
        "?provider_organizationId",
        "?provider_specialty",
        "?provider_utilization",
    ]

    return variables


def get_supply_variables() -> list:
    """
    Get variables of Supply class.
    """
    variables = [
        "?supply_code",
        "?supply_date" "?supply_description",
        "?supply_encounterId",
        "?supply_patientId",
        "?supply_quantity",
    ]

    return variables
