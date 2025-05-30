import pytest
import requests
from ehr_apis import (
    get_doc_reference_by_patient_id,
    get_doc_reference_by_patient_id_and_encounter_id,
    get_doc_reference_by_patient_id_encounter_id_and_date_range,
    update_document_reference,
    get_patient_by_id,
    update_patient,
    get_encounter_by_id,
    get_encounter_by_patient_id,
    get_encounter_by_patient_id_and_date_range,
    update_encounter,
    get_medication_request_by_patient_id,
    get_medication_request_by_id,
    update_medication_request,
    get_condition_by_patient_id,
    get_condition_by_patient_id_and_encounter_id,
    update_condition,
    get_observation_by_id,
    get_observation_by_patient_id,
    get_observation_by_patient_id_and_encounter_id,
    update_observation,
    create_binary,
    create_order_test,
    create_document_reference,
    create_patient,
    create_encounter,
    create_medication_request,
    create_condition,
    create_observation
)

def get_coligomed_token():
    url = "https://myhealth-api-dev.coligomed.com/userservice/coligomed-user/partner-login"
    headers = {
        "Content-Type": "application/json",
        "Cookie": "connect.sid=s%3AfLyaRwpbIYAwg5Z9-tDStz659SbQ8BbA.aLKB8C0OmB9rPFg4olmBGlJDcYdnRihpZODwR%2BknKAM"
    }
    data = {
        "user_name": "101genai@coligomed.com",
        "password": "Coligomed@223"
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def bearer_token():
    return get_coligomed_token()

# DocumentReference Tests
def test_get_doc_reference_by_patient_id(bearer_token, patient_id='1'):
    document_references = get_doc_reference_by_patient_id(bearer_token, patient_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(document_references) > 0, "No document references found for patient"

def test_get_doc_reference_by_patient_id_and_encounter_id(bearer_token, patient_id='1', encounter_id='1'):
    document_references = get_doc_reference_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(document_references) > 0, "No document references found for patient and encounter"

def test_get_doc_reference_by_patient_id_encounter_id_and_date_range(bearer_token, patient_id='1', encounter_id='1', start_date='2023-01-01', end_date='2023-12-31'):
    document_references = get_doc_reference_by_patient_id_encounter_id_and_date_range(bearer_token, patient_id, encounter_id, start_date, end_date, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(document_references) > 0, "No document references found for patient, encounter and date range"

def test_update_document_reference_and_verify(bearer_token, document_id='1203167'):
    # First get the original document reference data
    original_doc = get_doc_reference_by_patient_id(bearer_token, "1", base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")  # Get first document
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
    updated_response = update_document_reference(bearer_token, document_id, update_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_response is not None, "Update document reference failed"
    
    # Verify the update response
    assert updated_response["id"] == "1203167", "ID not updated correctly"
    assert updated_response["status"] == "current", "Status not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["date"] == "2025-01-04T08:30:00+00:00", "Date not updated correctly"
    assert updated_response["content"][0]["attachment"]["title"] == "Patient Clinical Notes", "Title not updated correctly"
    
    # Get the updated document reference
    updated_doc = get_doc_reference_by_patient_id(bearer_token, "1", base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_doc is not None, "No updated document reference found"
    
    # Compare with original
    assert updated_doc["id"] == original_doc["id"], "ID should remain unchanged"
    assert updated_doc["type"] == original_doc["type"], "Type should remain unchanged"

def test_create_document_reference_and_verify(bearer_token):
    # Create document reference data
    doc_data = {
        "resourceType": "DocumentReference",
        "status": "current",
        "docStatus": "final",
        "type": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/document-relationship-type",
                "code": "document",
                "display": "Document"
            }]
        },
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "clinical-note",
                "display": "Clinical Note"
            }]
        }],
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "date": "2025-01-04T08:30:00+00:00",
        "author": [{
            "reference": "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3",
            "display": "Family Medicine Physician, MD"
        }],
        "content": [{
            "attachment": {
                "contentType": "text/plain",
                "url": "http://example.com/notes/patient-lopez-note.txt",
                "title": "Patient Clinical Notes",
                "creation": "2025-01-04T08:30:00+00:00"
            }
        }]
    }
    
    # Create the document reference
    created_response = create_document_reference(bearer_token, doc_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert created_response is not None, "Create document reference failed"
    
    # Verify the create response
    assert created_response["resourceType"] == "DocumentReference", "Resource type not set correctly"
    assert created_response["status"] == "current", "Status not set correctly"
    assert created_response["subject"]["reference"] == "Patient/10434", "Subject reference not set correctly"
    assert created_response["date"] == "2025-01-04T08:30:00+00:00", "Date not set correctly"
    assert created_response["content"][0]["attachment"]["title"] == "Patient Clinical Notes", "Title not set correctly"

# Patient Tests
def test_get_patient_by_id(bearer_token, patient_id='1203165'):
    patient = get_patient_by_id(bearer_token, patient_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert patient is not None, "No patient found with given ID"

def test_update_patient_and_verify(bearer_token, patient_id='1203165'):
    # First get the original patient data
    original_patient = get_patient_by_id(bearer_token, patient_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
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
    updated_response = update_patient(bearer_token, patient_id, update_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_response is not None, "Update patient failed"
    
    # Verify the update response
    assert updated_response["id"] == "1203165", "ID not updated correctly"
    assert updated_response["name"][0]["family"] == "Doe", "Family name not updated correctly"
    assert updated_response["gender"] == "female", "Gender not updated correctly"
    assert updated_response["birthDate"] == "1985-05-15", "Birth date not updated correctly"
    assert updated_response["address"][0]["city"] == "New York", "City not updated correctly"
    assert updated_response["address"][0]["state"] == "NY", "State not updated correctly"

def test_create_patient_and_verify(bearer_token):
    # Create patient data
    patient_data = {
        "resourceType": "Patient",
        "identifier": [{
            "use": "official",
            "system": "http://hospital.smarthealthit.org",
            "value": "MRN12345"
        }],
        "name": [{
            "use": "official",
            "family": "Doe",
            "given": ["John"]
        }],
        "gender": "female",
        "birthDate": "1985-05-15",
        "address": [{
            "use": "home",
            "line": ["456 New St"],
            "city": "New York",
            "state": "NY",
            "postalCode": "10002"
        }]
    }
    
    # Create the patient
    created_response = create_patient(bearer_token, patient_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert created_response is not None, "Create patient failed"
    
    # Verify the create response
    assert created_response["resourceType"] == "Patient", "Resource type not set correctly"
    assert created_response["name"][0]["family"] == "Doe", "Family name not set correctly"
    assert created_response["gender"] == "female", "Gender not set correctly"
    assert created_response["birthDate"] == "1985-05-15", "Birth date not set correctly"
    assert created_response["address"][0]["city"] == "New York", "City not set correctly"

# Encounter Tests
def test_get_encounter_by_id(bearer_token, encounter_id='1203252'):
    encounter = get_encounter_by_id(bearer_token, encounter_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert encounter is not None, "No encounter found with given ID"

def test_get_encounter_by_patient_id(bearer_token, patient_id='1'):
    encounters = get_encounter_by_patient_id(bearer_token, patient_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(encounters) > 0, "No encounters found for patient"

def test_get_encounter_by_patient_id_and_date_range(bearer_token, patient_id='1', start_date='2023-01-01', end_date='2023-12-31'):
    encounters = get_encounter_by_patient_id_and_date_range(bearer_token, patient_id, start_date, end_date, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(encounters) > 0, "No encounters found for patient in date range"

def test_update_encounter_and_verify(bearer_token, encounter_id='1203252'):
    # First get the original encounter data
    original_encounter = get_encounter_by_id(bearer_token, encounter_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert original_encounter is not None, "No original encounter found with given ID"
    
    # Create update data
    update_data = {
        "resourceType": "Encounter",
        "id": "1203252",
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
    updated_response = update_encounter(bearer_token, encounter_id, update_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_response is not None, "Update encounter failed"
    
    # Verify the update response
    assert updated_response["id"] == "1203252", "ID not updated correctly"
    assert updated_response["status"] == "in-progress", "Status not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["period"]["start"] == "2021-05-28", "Period start not updated correctly"
    assert updated_response["period"]["end"] == "2021-05-28", "Period end not updated correctly"
    
    # Get the updated encounter
    updated_encounter = get_encounter_by_id(bearer_token, encounter_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_encounter is not None, "No updated encounter found"
    
    # Compare with original
    assert updated_encounter["id"] == original_encounter["id"], "ID should remain unchanged"
    assert updated_encounter["type"] == original_encounter["type"], "Type should remain unchanged"

def test_create_encounter_and_verify(bearer_token):
    # Create encounter data
    encounter_data = {
        "resourceType": "Encounter",
        "status": "in-progress",
        "class": {
            "system": "urn:oid:1.2.840.114350.1.72.1.7.7.10.696784.13260",
            "code": "13",
            "display": "Support OP Encounter"
        },
        "type": [{
            "coding": [{
                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.10.698084.30",
                "code": "101",
                "display": "Office Visit"
            }],
            "text": "Office Visit"
        }],
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "participant": [{
            "individual": {
                "reference": "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3",
                "type": "Practitioner",
                "display": "Family Medicine Physician, MD"
            }
        }],
        "period": {
            "start": "2021-05-28",
            "end": "2021-05-28"
        },
        "location": [{
            "location": {
                "display": "EMC Family Medicine"
            }
        }]
    }
    
    # Create the encounter
    created_response = create_encounter(bearer_token, encounter_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert created_response is not None, "Create encounter failed"
    
    # Verify the create response
    assert created_response["resourceType"] == "Encounter", "Resource type not set correctly"
    assert created_response["status"] == "in-progress", "Status not set correctly"
    assert created_response["subject"]["reference"] == "Patient/10434", "Subject reference not set correctly"
    assert created_response["period"]["start"] == "2021-05-28", "Period start not set correctly"
    assert created_response["period"]["end"] == "2021-05-28", "Period end not set correctly"

# MedicationRequest Tests
def test_get_medication_request_by_patient_id(bearer_token, patient_id='1'):
    medication_requests = get_medication_request_by_patient_id(bearer_token, patient_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(medication_requests) > 0, "No medication requests found for patient"

def test_get_medication_request_by_id(bearer_token, medication_request_id='1210332'):
    medication_request = get_medication_request_by_id(bearer_token, medication_request_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert medication_request is not None, "No medication request found with given ID"

def test_update_medication_request_and_verify(bearer_token, medication_request_id='1210332'):
    # First get the original medication request data
    original_medication_request = get_medication_request_by_id(bearer_token, medication_request_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert original_medication_request is not None, "No original medication request found with given ID"
    
    # Create update data
    update_data = {
        "resourceType": "MedicationRequest",
        "id": medication_request_id,
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [{
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "1049630",
                "display": "Amoxicillin 500mg"
            }]
        },
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "encounter": {
            "reference": "Encounter/1203252"
        },
        "authoredOn": "2025-01-03T08:00:00+00:00",
        "dosageInstruction": [{
            "text": "Take one tablet three times daily",
            "timing": {
                "repeat": {
                    "frequency": 3,
                    "period": 1,
                    "periodUnit": "d"
                }
            }
        }],
        "dispenseRequest": {
            "quantity": {
                "value": 60,
                "unit": "tablets"
            }
        }
    }
    
    # Update the medication request
    updated_response = update_medication_request(bearer_token, medication_request_id, update_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_response is not None, "Update medication request failed"
    
    # Verify the update response
    assert updated_response["id"] == medication_request_id, "ID not updated correctly"
    assert updated_response["status"] == "active", "Status not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["authoredOn"] == "2025-01-03T08:00:00+00:00", "Authored date not updated correctly"
    assert updated_response["dosageInstruction"][0]["text"] == "Take one tablet three times daily", "Dosage instruction not updated correctly"
    
    # Get the updated medication request
    updated_medication_request = get_medication_request_by_id(bearer_token, medication_request_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_medication_request is not None, "No updated medication request found"
    
    # Compare with original
    assert updated_medication_request["id"] == original_medication_request["id"], "ID should remain unchanged"
    assert updated_medication_request["medicationCodeableConcept"] == original_medication_request["medicationCodeableConcept"], "Medication concept should remain unchanged"

def test_create_medication_request_and_verify(bearer_token):
    # Create medication request data
    med_request_data = {
        "resourceType": "MedicationRequest",
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [{
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "1049630",
                "display": "Amoxicillin 500mg"
            }]
        },
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "encounter": {
            "reference": "Encounter/1203252"
        },
        "authoredOn": "2025-01-03T08:00:00+00:00",
        "dosageInstruction": [{
            "text": "Take one tablet three times daily",
            "timing": {
                "repeat": {
                    "frequency": 3,
                    "period": 1,
                    "periodUnit": "d"
                }
            }
        }],
        "dispenseRequest": {
            "quantity": {
                "value": 60,
                "unit": "tablets"
            }
        }
    }
    
    # Create the medication request
    created_response = create_medication_request(bearer_token, med_request_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert created_response is not None, "Create medication request failed"
    
    # Verify the create response
    assert created_response["resourceType"] == "MedicationRequest", "Resource type not set correctly"
    assert created_response["status"] == "active", "Status not set correctly"
    assert created_response["medicationCodeableConcept"]["coding"][0]["code"] == "1049630", "Medication code not set correctly"
    assert created_response["subject"]["reference"] == "Patient/10434", "Subject reference not set correctly"
    assert created_response["dosageInstruction"][0]["text"] == "Take one tablet three times daily", "Dosage instruction not set correctly"

# Condition Tests
def test_get_condition_by_patient_id(bearer_token, patient_id='1'):
    conditions = get_condition_by_patient_id(bearer_token, patient_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(conditions) > 0, "No conditions found for patient"

def test_get_condition_by_patient_id_and_encounter_id(bearer_token, patient_id='1', encounter_id='1'):
    conditions = get_condition_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(conditions) > 0, "No conditions found for patient and encounter"

def test_update_condition_and_verify(bearer_token, condition_id='1210331'):
    # First get the original condition data
    original_condition = get_condition_by_patient_id(bearer_token, "1", base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")  # Get first condition
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
    updated_response = update_condition(bearer_token, condition_id, update_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_response is not None, "Update condition failed"
    
    # Verify the update response
    assert updated_response["id"] == condition_id, "ID not updated correctly"
    assert updated_response["clinicalStatus"]["coding"][0]["code"] == "active", "Clinical status not updated correctly"
    assert updated_response["verificationStatus"]["coding"][0]["code"] == "confirmed", "Verification status not updated correctly"
    
    # Get the updated condition
    updated_condition = get_condition_by_patient_id(bearer_token, "1", base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_condition is not None, "No updated condition found"
    
    # Compare with original
    assert updated_condition["id"] == original_condition["id"], "ID should remain unchanged"
    # assert updated_condition["code"] == original_condition["code"], "Code should remain unchanged"

def test_create_condition_and_verify(bearer_token):
    # Create condition data
    condition_data = {
        "resourceType": "Condition",
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active",
                "display": "Active"
            }]
        },
        "verificationStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed",
                "display": "Confirmed"
            }]
        },
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                "code": "encounter-diagnosis",
                "display": "Encounter Diagnosis"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "44054006",
                "display": "Diabetes mellitus type 2"
            }]
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
    
    # Create the condition
    created_response = create_condition(bearer_token, condition_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert created_response is not None, "Create condition failed"
    
    # Verify the create response
    assert created_response["resourceType"] == "Condition", "Resource type not set correctly"
    assert created_response["clinicalStatus"]["coding"][0]["code"] == "active", "Clinical status not set correctly"
    assert created_response["code"]["coding"][0]["code"] == "44054006", "Condition code not set correctly"
    assert created_response["subject"]["reference"] == "Patient/10434", "Subject reference not set correctly"
    assert created_response["recordedDate"] == "2025-01-03T08:00:00+00:00", "Recorded date not set correctly"

# Observation Tests

def test_get_observation_by_id(bearer_token, observation_id='1203308'):
    observations = get_observation_by_id(bearer_token, observation_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(observations) > 0, "No observations found for patient"

def test_get_observation_by_patient_id(bearer_token, patient_id='1'):
    observations = get_observation_by_patient_id(bearer_token, patient_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(observations) > 0, "No observations found for patient"

def test_get_observation_by_patient_id_and_encounter_id(bearer_token, patient_id='1', encounter_id='1'):
    observations = get_observation_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert len(observations) > 0, "No observations found for patient and encounter"

def test_update_observation_and_verify(bearer_token, observation_id='1203308'):
    # First get the original observation data
    original_observation = get_observation_by_patient_id(bearer_token, "1", base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")  # Get first observation
    assert original_observation is not None, "No original observation found"
    
    # Create update data
    update_data = {
        "resourceType": "Observation",
        "id": observation_id,
        "meta": {
            "versionId": "2",
            "lastUpdated": "2025-01-04T08:30:00+00:00"
        },
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "laboratory",
                "display": "Laboratory"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "2339-0",
                "display": "Blood pressure panel"
            }]
        },
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "effectiveDateTime": "2025-01-03T08:00:00+00:00",
        "issued": "2025-01-03T09:00:00+00:00",
        "performer": [{
            "reference": "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3",
            "display": "Family Medicine Physician, MD"
        }],
        "valueQuantity": {
            "value": 120,
            "unit": "mmHg",
            "system": "http://unitsofmeasure.org",
            "code": "mm[Hg]"
        },
        "interpretation": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                "code": "N",
                "display": "Normal"
            }]
        }]
    }
    
    # Update the observation
    updated_response = update_observation(bearer_token, observation_id, update_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_response is not None, "Update observation failed"
    
    # Verify the update response
    assert updated_response["id"] == observation_id, "ID not updated correctly"
    assert updated_response["status"] == "final", "Status not updated correctly"
    assert updated_response["subject"]["reference"] == "Patient/10434", "Subject reference not updated correctly"
    assert updated_response["effectiveDateTime"] == "2025-01-03T08:00:00+00:00", "Effective date not updated correctly"
    assert updated_response["valueQuantity"]["value"] == 120, "Value not updated correctly"
    
    # Get the updated observation
    updated_observation = get_observation_by_patient_id(bearer_token, "1", base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert updated_observation is not None, "No updated observation found"
    
    # Compare with original
    assert updated_observation["id"] == original_observation["id"], "ID should remain unchanged"
    # assert updated_observation["code"] == original_observation["code"], "Code should remain unchanged"
    #assert updated_observation["category"] == original_observation["category"], "Category should remain unchanged"

def test_create_observation_and_verify(bearer_token):
    # Create observation data
    observation_data = {
        "resourceType": "Observation",
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "laboratory",
                "display": "Laboratory"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "2339-0",
                "display": "Blood pressure panel"
            }]
        },
        "subject": {
            "reference": "Patient/10434",
            "display": "Lopez, Camila Maria"
        },
        "effectiveDateTime": "2025-01-03T08:00:00+00:00",
        "issued": "2025-01-03T09:00:00+00:00",
        "performer": [{
            "reference": "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3",
            "display": "Family Medicine Physician, MD"
        }],
        "valueQuantity": {
            "value": 120,
            "unit": "mmHg",
            "system": "http://unitsofmeasure.org",
            "code": "mm[Hg]"
        },
        "interpretation": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                "code": "N",
                "display": "Normal"
            }]
        }]
    }
    
    # Create the observation
    created_response = create_observation(bearer_token, observation_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert created_response is not None, "Create observation failed"
    
    # Verify the create response
    assert created_response["resourceType"] == "Observation", "Resource type not set correctly"
    assert created_response["status"] == "final", "Status not set correctly"
    assert created_response["valueQuantity"]["value"] == 120, "Value not set correctly"
    assert created_response["subject"]["reference"] == "Patient/10434", "Subject reference not set correctly"
    assert created_response["effectiveDateTime"] == "2025-01-03T08:00:00+00:00", "Effective date not set correctly"

# Binary Tests
def test_create_binary_and_verify(bearer_token):
    # Create binary data
    binary_data = {
        "resourceType": "Binary",
        "contentType": "text/plain",
        "data": "SGVsbG8sIHRoaXMgaXMgYSBzYW1wbGUgdGV4dCBmaWxlLg=="  # Base64 encoded PDF data
    }
    
    # Create the binary
    created_response = create_binary(bearer_token, binary_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert created_response is not None and created_response != {}, "Create binary failed"
    
    # Verify the create response
    assert created_response["resourceType"] == "Binary", "Resource type not set correctly"
    assert created_response["contentType"] == "text/plain", "Content type not set correctly"
    assert created_response["data"] == binary_data["data"], "Data not set correctly"

# Order Test Tests
def test_create_order_test_and_verify(bearer_token):
    # Create order test data
    order_test_data = {
        "resourceType": "ServiceRequest",
        "status": "active",
        "intent": "order",
        "category": [ {
            "coding": [ {
                "system": "http://terminology.hl7.org/CodeSystem/service-type",
                "code": "108252007",
                "display": "Laboratory procedure"
            } ]
        } ],
        "code": {
            "coding": [ {
                "system": "http://loinc.org",
                "code": "58410-2",
                "display": "Complete Blood Count (CBC) panel"
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
        "requester": {
            "reference": "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3",
            "display": "Family Medicine Physician, MD"
        }
    }
    
    # Create the order test
    created_response = create_order_test(bearer_token, order_test_data, base_url="https://myhealth-api-dev.coligomed.com/partners/healthrecordsfhir/fhir")
    assert created_response is not None, "Create order test failed"
    
    # Verify the create response
    assert created_response["resourceType"] == "ServiceRequest", "Resource type not set correctly"
    assert created_response["status"] == "active", "Status not set correctly"
    assert created_response["intent"] == "order", "Intent not set correctly"
    assert created_response["code"]["coding"][0]["code"] == "58410-2", "Test code not set correctly"
    assert created_response["subject"]["reference"] == "Patient/10434", "Subject reference not set correctly"
    assert created_response["encounter"]["reference"] == "Encounter/1203252", "Encounter reference not set correctly"
    #assert created_response["authoredOn"] == "2025-01-03T08:00:00+00:00", "Authored date not set correctly"
    assert created_response["requester"]["reference"] == "Practitioner/testeM5CWtq15N0WJeuCet5bJlQ3", "Requester reference not set correctly"