# test_ehr_apis.py


import pytest
import requests
import yaml
from unittest.mock import patch, MagicMock
from pytest_check import check
from utils import get_bearer_token

import ehr_apis
from ehr_apis import (
    get_doc_reference_by_patient_id,
    get_doc_reference_by_patient_id_and_encounter_id,
    get_doc_reference_by_patient_id_encounter_id_and_date_range,
    get_patient_by_id,
    get_encounter_by_id,
    get_encounter_by_patient_id,
    get_encounter_by_patient_id_and_date_range,
    get_medication_request_by_patient_id,
    get_medication_request_by_id,
    get_condition_by_patient_id,
    get_condition_by_patient_id_and_encounter_id,
    get_observation_by_patient_id,
    get_observation_by_patient_id_and_encounter_id,
    update_encounter,
    update_medication_request,
    update_condition,
    update_observation,
    update_document_reference,
    update_patient
)


# @pytest.mark.parametrize(
# 	"get_bearer_token",
# 	[
# 		{
# 			"url": "https://ea.api.101gen.ai/login",
# 			"client_side": False,
# 			"username": "qa_low_username",
# 			"password": "qa_low_password",
# 		}
# 	],
# 	indirect=True
# )
# def test_get_encounter_by_patient_id(get_bearer_token, patient_id='1'):
#     bearer_token = get_bearer_token
#     encounters = ehr_apis.get_encounter_by_patient_id(bearer_token, patient_id) 
#     assert len(encounters) > 0, "No encounters found for patient"
    
# =============================================
# DocumentReference Tests
# =============================================

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_doc_reference_by_patient_id(get_bearer_token, patient_id='1'):
    bearer_token = get_bearer_token
    document_references = ehr_apis.get_doc_reference_by_patient_id(bearer_token, patient_id)
    assert len(document_references) > 0, "No document references found for patient"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_doc_reference_by_patient_id_and_encounter_id(get_bearer_token, patient_id='1', encounter_id='1'):
    bearer_token = get_bearer_token
    document_references = ehr_apis.get_doc_reference_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id)
    assert len(document_references) > 0, "No document references found for patient and encounter"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_doc_reference_by_patient_id_encounter_id_and_date_range(get_bearer_token, patient_id='1', encounter_id='1', start_date='2023-01-01', end_date='2023-12-31'):
    bearer_token = get_bearer_token
    document_references = ehr_apis.get_doc_reference_by_patient_id_encounter_id_and_date_range(bearer_token, patient_id, encounter_id, start_date, end_date)
    assert len(document_references) > 0, "No document references found for patient, encounter and date range"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_update_document_reference_and_verify(get_bearer_token, document_id='1203167'):
    bearer_token = get_bearer_token
    
    # First get the original document reference data
    original_doc = ehr_apis.get_doc_reference_by_patient_id(bearer_token, "1")  # Get first document
    assert original_doc is not None, "No original document reference found"
    
    # Create update data
    update_data = {
        "resourceType": "DocumentReference",
        "id": "1203167",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2025-01-04T08:29:58.378+00:00"
        },
        "status": "current",
        "docStatus": "final",
        "type": {
            "coding": [ {
                "system": "http://terminology.hl7.org/CodeSystem/document-relationship-type",
                "code": "document",
                "display": "Document"
            } ]
        },
        "category": [ {
            "coding": [ {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "clinical-note",
                "display": "Clinical Note"
            } ]
        } ],
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "date": "2025-01-04T08:30:00+00:00",
        "author": [ {
            "reference": "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3",
            "display": "Family Medicine Physician, MD"
        } ],
        "content": [ {
            "attachment": {
                "contentType": "text/plain",
                "url": "http://example.com/notes/patient-lopez-note.txt",
                "title": "Patient Clinical Notes",
                "creation": "2025-01-04T08:30:00+00:00"
            }
        } ]
    }
    
    # Update the document reference
    updated_response = ehr_apis.update_document_reference(bearer_token, document_id, update_data)
    assert updated_response is not None, "Update document reference failed"
    
    # Verify the update response
    assert updated_response["id"] == "1203167", "ID not updated correctly"
    #assert updated_response["meta"]["versionId"] == "1", "Version ID not updated correctly"
    #assert updated_response["meta"]["lastUpdated"] == "2025-01-04T08:29:58.378+00:00", "Last updated timestamp not updated correctly"
    assert updated_response["status"] == "current", "Status not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["date"] == "2025-01-04T08:30:00+00:00", "Date not updated correctly"
    assert updated_response["content"][0]["attachment"]["title"] == "Patient Clinical Notes", "Title not updated correctly"
    
    # Get the updated document reference
    updated_doc = ehr_apis.get_doc_reference_by_patient_id(bearer_token, "1")
    assert updated_doc is not None, "No updated document reference found"
    
    # Compare with original
    assert updated_doc["id"] == original_doc["id"], "ID should remain unchanged"
    assert updated_doc["type"] == original_doc["type"], "Type should remain unchanged"
    #assert updated_doc["category"] == original_doc["category"], "Category should remain unchanged"
    
    


# =============================================
# Patient Tests
# =============================================

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_patient_by_id(get_bearer_token, patient_id='1203165'):
    bearer_token = get_bearer_token
    patient = ehr_apis.get_patient_by_id(bearer_token, patient_id)
    assert patient is not None, "No patient found with given ID"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_update_patient_and_verify(get_bearer_token, patient_id='1203165'):
    bearer_token = get_bearer_token
    
    # First get the original patient data
    original_patient = ehr_apis.get_patient_by_id(bearer_token, patient_id)
    assert original_patient is not None, "No original patient found with given ID"
    
    # Create update data
    update_data = {
        "resourceType": "Patient",
        "id": "1203165",
        "identifier": [ {
            "use": "official",
            "system": "http://hospital.smarthealthit.org",
            "value": "MRN12345"
        } ],
        "name": [ {
            "use": "official",
            "family": "Doe",
            "given": ["John"]
        } ],
        "gender": "female",
        "birthDate": "1985-05-15",
        "address": [ {
            "use": "home",
            "line": ["456 New St"],
            "city": "New York",
            "state": "NY",
            "postalCode": "10002"
        } ]
    }
    
    # Update the patient
    updated_response = ehr_apis.update_patient(bearer_token, patient_id, update_data)
    assert updated_response is not None, "Update patient failed"
    
    # Verify the update response
    assert updated_response["id"] == "1203165", "ID not updated correctly"
    assert updated_response["name"][0]["family"] == "Doe", "Family name not updated correctly"
    assert updated_response["gender"] == "female", "Gender not updated correctly"
    assert updated_response["birthDate"] == "1985-05-15", "Birth date not updated correctly"
    assert updated_response["address"][0]["city"] == "New York", "City not updated correctly"
    assert updated_response["address"][0]["state"] == "NY", "State not updated correctly"
    assert updated_response["address"][0]["postalCode"] == "10002", "Postal code not updated correctly"
    
    # Get the updated patient
    updated_patient = ehr_apis.get_patient_by_id(bearer_token, patient_id)
    assert updated_patient is not None, "No updated patient found with given ID"
    
    # Compare with original
    assert updated_patient["id"] == original_patient["id"], "ID should remain unchanged"
    assert updated_patient["identifier"][0]["value"] == original_patient["identifier"][0]["value"], "Identifier should remain unchanged"

# =============================================
# Encounter Tests
# =============================================

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_encounter_by_id(get_bearer_token, encounter_id='1203252'):
    bearer_token = get_bearer_token
    encounter = ehr_apis.get_encounter_by_id(bearer_token, encounter_id)
    assert encounter is not None, "No encounter found with given ID"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_encounter_by_patient_id(get_bearer_token, patient_id='1'):
    bearer_token = get_bearer_token
    encounters = ehr_apis.get_encounter_by_patient_id(bearer_token, patient_id)
    assert len(encounters) > 0, "No encounters found for patient"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "https://ea.api.101gen.ai/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_encounter_by_patient_id_and_date_range(get_bearer_token, patient_id='1', start_date='2023-01-01', end_date='2023-12-31'):
    bearer_token = get_bearer_token
    encounters = ehr_apis.get_encounter_by_patient_id_and_date_range(bearer_token, patient_id, start_date, end_date)
    assert len(encounters) > 0, "No encounters found for patient in date range"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_update_encounter_and_verify(get_bearer_token, encounter_id='1203252'):
    bearer_token = get_bearer_token
    
    # First get the original encounter data
    original_encounter = ehr_apis.get_encounter_by_id(bearer_token, encounter_id)
    assert original_encounter is not None, "No original encounter found with given ID"
    
    # Create update data
    update_data = {
     "resourceType": "Encounter",
     "id":"1203252",
     "meta": {
       "versionId": "1",
       "lastUpdated": "2022-04-11T08:37:02.069+00:00",
       "source": "#E5TFiaSdm813st7p"
     },
     "identifier": [ {
       "use": "usual",
       "system": "urn:oid:1.2.840.114350.1.13.0.1.7.3.698084.8",
       "value": "27558"
     } ],
     "status": "in-progress",
     "class": {
       "system": "urn:oid:1.2.840.114350.1.72.1.7.7.10.696784.13260",
       "code": "13",
       "display": "Support OP Encounter"
     },
     "type": [ {
       "coding": [ {
         "system": "urn:oid:1.2.840.114350.1.13.0.1.7.10.698084.30",
         "code": "101",
         "display": "Office Visit"
       } ],
       "text": "Office Visit"
     } ],
     "subject": {
       "reference": "Patient/10434",
       "display": "Lopez, Camila Maria"
     },
     "participant": [ {
       "individual": {
         "reference": "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3",
         "type": "Practitioner",
         "display": "Family Medicine Physician, MD"
       }
     } ],
     "period": {
       "start": "2021-05-28",
       "end": "2021-05-28"
     },
     "location": [ {
       "location": {
         "display": "EMC Family Medicine"
       }
     } ]
   }
    
    # Update the encounter
    updated_response = ehr_apis.update_encounter(bearer_token, encounter_id, update_data)
    assert updated_response is not None, "Update encounter failed"
    
    # Verify the update response
    assert updated_response["id"] == "1203252", "ID not updated correctly"
    assert updated_response["status"] == "in-progress", "Status not updated correctly"
    #assert updated_response["meta"]["versionId"] == "1", "Version ID not updated correctly"
    #assert updated_response["meta"]["lastUpdated"] == "2022-04-11T08:37:02.069+00:00", "Last updated timestamp not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["period"]["start"] == "2021-05-28", "Period start not updated correctly"
    assert updated_response["period"]["end"] == "2021-05-28", "Period end not updated correctly"
    
    # Get the updated encounter
    updated_encounter = ehr_apis.get_encounter_by_id(bearer_token, encounter_id)
    assert updated_encounter is not None, "No updated encounter found with given ID"
    
    # Compare with original
    assert updated_encounter["id"] == original_encounter["id"], "ID should remain unchanged"
    assert updated_encounter["class"] == original_encounter["class"], "Class should remain unchanged"
    assert updated_encounter["type"] == original_encounter["type"], "Type should remain unchanged"

# =============================================
# MedicationRequest Tests
# =============================================

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_medication_request_by_patient_id(get_bearer_token, patient_id='1'):
    bearer_token = get_bearer_token
    medication_requests = ehr_apis.get_medication_request_by_patient_id(bearer_token, patient_id)
    assert len(medication_requests) > 0, "No medication requests found for patient"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_medication_request_by_id(get_bearer_token, medication_request_id='1210332'):
    bearer_token = get_bearer_token
    medication_request = ehr_apis.get_medication_request_by_id(bearer_token, medication_request_id)
    assert medication_request is not None, "No medication request found with given ID"

# =============================================
# Condition Tests
# =============================================

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_condition_by_patient_id(get_bearer_token, patient_id='1'):
    bearer_token = get_bearer_token
    conditions = ehr_apis.get_condition_by_patient_id(bearer_token, patient_id)
    assert len(conditions) > 0, "No conditions found for patient"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_condition_by_patient_id_and_encounter_id(get_bearer_token, patient_id='1', encounter_id='1'):
    bearer_token = get_bearer_token
    conditions = ehr_apis.get_condition_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id)
    assert len(conditions) > 0, "No conditions found for patient and encounter"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_update_condition_and_verify(get_bearer_token, condition_id='1210331'):
    bearer_token = get_bearer_token
    
    # First get the original condition data
    original_condition = ehr_apis.get_condition_by_patient_id(bearer_token, "1")  # Get first condition
    assert original_condition is not None, "No original condition found"
    
    # Create update data
    update_data = {
        "resourceType": "Condition",
        "id": "1210331",
        "meta": {
            "versionId": "1",
            "lastUpdated": "2025-01-30T16:49:12.937+00:00"
        },
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active",
                    "display": "Active"
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "confirmed",
                    "display": "Confirmed"
                }
            ]
        },
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                        "code": "encounter-diagnosis",
                        "display": "Encounter Diagnosis"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "44054006",
                    "display": "Diabetes mellitus type 2"
                }
            ]
        },
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "encounter": {
            "reference": "Encounter/1203252"
        },
        "recordedDate": "2025-01-03T08:00:00+00:00"
    }
    
    # Update the condition
    updated_response = ehr_apis.update_condition(bearer_token, condition_id, update_data)
    assert updated_response is not None, "Update condition failed"
    
    # Verify the update response
    assert updated_response["id"] == "1210331", "ID not updated correctly"
    #assert updated_response["meta"]["versionId"] == "1", "Version ID not updated correctly"
    #assert updated_response["meta"]["lastUpdated"] == "2025-01-30T16:49:12.937+00:00", "Last updated timestamp not updated correctly"
    assert updated_response["clinicalStatus"]["coding"][0]["code"] == "active", "Clinical status not updated correctly"
    assert updated_response["code"]["coding"][0]["code"] == "44054006", "Condition code not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["encounter"]["reference"] == "Encounter/1203252", "Encounter reference not updated correctly"
    assert updated_response["recordedDate"] == "2025-01-03T08:00:00+00:00", "Recorded date not updated correctly"
    
    # Get the updated condition
    updated_condition = ehr_apis.get_condition_by_patient_id(bearer_token, "1")
    assert updated_condition is not None, "No updated condition found"
    
    # Compare with original
    assert updated_condition["id"] == original_condition["id"], "ID should remain unchanged"
    #assert updated_condition["verificationStatus"] == original_condition["verificationStatus"], "Verification status should remain unchanged"

# =============================================
# Observation Tests
# =============================================

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_observation_by_id(get_bearer_token, observation_id='1203308'):
    bearer_token = get_bearer_token
    observations = ehr_apis.get_observation_by_id(bearer_token, observation_id)
    assert len(observations) > 0, "No observations found for patient"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_observation_by_patient_id(get_bearer_token, patient_id='1'):
    bearer_token = get_bearer_token
    observations = ehr_apis.get_observation_by_patient_id(bearer_token, patient_id)
    assert len(observations) > 0, "No observations found for patient"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_get_observation_by_patient_id_and_encounter_id(get_bearer_token, patient_id='1', encounter_id='1'):
    bearer_token = get_bearer_token
    observations = ehr_apis.get_observation_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id)
    assert len(observations) > 0, "No observations found for patient and encounter"

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_update_observation_and_verify(get_bearer_token, observation_id='1203308'):
    bearer_token = get_bearer_token
    
    # First get the original observation data
    original_observation = ehr_apis.get_observation_by_id(bearer_token, observation_id)  # Get first observation
    assert original_observation is not None, "No original observation found"
    
    # Create update data
    update_data = {
        "resourceType": "Observation",
        "id": "1203308",
        "meta": {
            "versionId": "2",
            "lastUpdated": "2025-01-04T08:30:00+00:00"
        },
        "status": "final",
        "category": [ {
            "coding": [ {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "laboratory",
                "display": "Laboratory"
            } ]
        } ],
        "code": {
            "coding": [ {
                "system": "http://loinc.org",
                "code": "2339-0",
                "display": "Blood pressure panel"
            } ]
        },
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "effectiveDateTime": "2025-01-03T08:00:00+00:00",
        "issued": "2025-01-03T09:00:00+00:00",
        "performer": [ {
            "reference": "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3",
            "display": "Family Medicine Physician, MD"
        } ],
        "valueQuantity": {
            "value": 120,
            "unit": "mmHg",
            "system": "http://unitsofmeasure.org",
            "code": "mm[Hg]"
        },
        "interpretation": [ {
            "coding": [ {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                "code": "N",
                "display": "Normal"
            } ]
        } ]
    }
    
    # Update the observation
    updated_response = ehr_apis.update_observation(bearer_token, observation_id, update_data)
    assert updated_response is not None, "Update observation failed"
    
    # Verify the update response
    assert updated_response["id"] == "1203308", "ID not updated correctly"
    assert updated_response["meta"]["versionId"] == "2", "Version ID not updated correctly"
    #assert updated_response["meta"]["lastUpdated"] == "2025-01-04T08:30:00+00:00", "Last updated timestamp not updated correctly"
    assert updated_response["status"] == "final", "Status not updated correctly"
    assert updated_response["valueQuantity"]["value"] == 120, "Value not updated correctly"
    assert updated_response["interpretation"][0]["coding"][0]["code"] == "N", "Interpretation not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["effectiveDateTime"] == "2025-01-03T08:00:00+00:00", "Effective date not updated correctly"
    
    # Get the updated observation
    updated_observation = ehr_apis.get_observation_by_id(bearer_token, observation_id)
    assert updated_observation is not None, "No updated observation found"
    
    # Compare with original
    assert updated_observation["id"] == original_observation["id"], "ID should remain unchanged"
    assert updated_observation["code"] == original_observation["code"], "Code should remain unchanged"
    assert updated_observation["category"] == original_observation["category"], "Category should remain unchanged"

# =============================================
# MedicationRequest Tests
# =============================================

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_update_medication_request_and_verify(get_bearer_token, medication_request_id='1210332'):
    bearer_token = get_bearer_token
    
    # First get the original medication request data
    original_med_request = ehr_apis.get_medication_request_by_id(bearer_token, medication_request_id)  # Get first medication request
    assert original_med_request is not None, "No original medication request found"
    
    # Create update data
    update_data = {
        "resourceType": "MedicationRequest",
        "id": "1210332",
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [ {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "1049630",
                "display": "Amoxicillin 500mg"
            } ]
        },
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "encounter": {
            "reference": "Encounter/1203252"
        },
        "authoredOn": "2025-01-03T08:00:00+00:00",
        "dosageInstruction": [ {
            "text": "Take one tablet three times daily",
            "timing": {
                "repeat": {
                    "frequency": 3,
                    "period": 1,
                    "periodUnit": "d"
                }
            }
        } ],
        "dispenseRequest": {
            "quantity": {
                "value": 60,
                "unit": "tablets"
            }
        }
    }
    
    # Update the medication request
    updated_response = ehr_apis.update_medication_request(bearer_token, medication_request_id, update_data)
    assert updated_response is not None, "Update medication request failed"
    
    # Verify the update response
    assert updated_response["id"] == "1210332", "ID not updated correctly"
    assert updated_response["status"] == "active", "Status not updated correctly"
    assert updated_response["medicationCodeableConcept"]["coding"][0]["code"] == "1049630", "Medication code not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["encounter"]["reference"] == "Encounter/1203252", "Encounter reference not updated correctly"
    assert updated_response["authoredOn"] == "2025-01-03T08:00:00+00:00", "Authored date not updated correctly"
    assert updated_response["dosageInstruction"][0]["text"] == "Take one tablet three times daily", "Dosage instruction not updated correctly"
    assert updated_response["dispenseRequest"]["quantity"]["value"] == 60, "Quantity not updated correctly"
    
    # Get the updated medication request
    updated_med_request = ehr_apis.get_medication_request_by_id(bearer_token, medication_request_id)
    assert updated_med_request is not None, "No updated medication request found"
    
    # Compare with original
    assert updated_med_request["id"] == original_med_request["id"], "ID should remain unchanged"
    assert updated_med_request["intent"] == original_med_request["intent"], "Intent should remain unchanged"
    assert updated_med_request["medicationCodeableConcept"] == original_med_request["medicationCodeableConcept"], "Medication should remain unchanged"

