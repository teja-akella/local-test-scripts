# ehr_apis.py

import requests

# =============================================
# DocumentReference Functions
# =============================================

def get_doc_reference_by_patient_id(bearer_token, patient_id, base_url="http://localhost:5173/ehr"):
    url = f"{base_url}/DocumentReference?patient={patient_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Document Reference by Patient ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Document Reference by Patient ID retrieved successfully.")

    return response.json()


def get_doc_reference_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id, base_url="http://localhost:5173/ehr"):
    url = f"{base_url}/DocumentReference?patient={patient_id}&encounter={encounter_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Document Reference by Patient ID and Encounter ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Document Reference by Patient ID and Encounter ID retrieved successfully.")

    return response.json()


def get_doc_reference_by_patient_id_encounter_id_and_date_range(bearer_token, patient_id, encounter_id, start_date, end_date, base_url="http://localhost:5173/ehr"):
    url = f"{base_url}/DocumentReference?patient={patient_id}&encounter={encounter_id}&date=ge{start_date}&date=le{end_date}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Document Reference by Patient ID, Encounter ID and Date Range...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Document Reference by Patient ID, Encounter ID and Date Range retrieved successfully.")

    return response.json()


def update_document_reference(bearer_token, document_id, data=None, base_url="http://localhost:5173/update_ehr"):
    url = f"{base_url}/DocumentReference/{document_id}"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "DocumentReference",
            "id": "1203167",
            "meta": {
                "versionId": "1",
                "lastUpdated": "2025-01-04T08:29:58.378+00:00"
            },
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

    # Send and check request
    print(f"\nSending PUT request to {url}. Updating Document Reference with ID: {document_id}")
    response = requests.put(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Document Reference updated successfully.")

    return response.json()


def create_document_reference(bearer_token, data=None, base_url="http://localhost:5173/add_ehr"):
    url = f"{base_url}/DocumentReference"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "DocumentReference",
            "meta": {
                "versionId": "1",
                "lastUpdated": "2025-01-04T08:29:58.378+00:00"
            },
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

    # Send and check request
    print(f"\nSending POST request to {url}. Creating new Document Reference")
    response = requests.post(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Document Reference created successfully.")

    return response.json()


# =============================================
# Patient Functions
# =============================================

def get_patient_by_id(bearer_token, patient_id, base_url="http://localhost:5173/ehr"):
    url = f"{base_url}/Patient/{patient_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Patient details...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Patient details retrieved successfully.")

    return response.json()


def update_patient(bearer_token, patient_id, data=None, base_url="http://localhost:5173/update_ehr"):
    url = f"{base_url}/Patient/{patient_id}"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "Patient",
            "id": patient_id,
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

    # Send and check request
    print(f"\nSending PUT request to {url}. Updating Patient with ID: {patient_id}")
    response = requests.put(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Patient updated successfully.")

    return response.json()


def create_patient(bearer_token, data=None, base_url="http://localhost:5173/add_ehr"):
    url = f"{base_url}/Patient"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
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

    # Send and check request
    print(f"\nSending POST request to {url}. Creating new Patient")
    response = requests.post(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Patient created successfully.")

    return response.json()


# =============================================
# Encounter Functions
# =============================================

def get_encounter_by_id(bearer_token, encounter_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/Encounter/{encounter_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Encounter details...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Encounter details retrieved successfully.")

    return response.json()


def get_encounter_by_patient_id(bearer_token, patient_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/Encounter?patient={patient_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Encounters by Patient ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Encounters retrieved successfully.")

    return response.json()


def get_encounter_by_patient_id_and_date_range(bearer_token, patient_id, start_date, end_date, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/Encounter?patient={patient_id}&date=ge{start_date}&date=le{end_date}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Encounters by Patient ID and Date Range...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Encounters retrieved successfully.")

    return response.json()


def update_encounter(bearer_token, encounter_id, data=None, base_url="https://ea.api.101gen.ai/update_ehr"):
    url = f"{base_url}/Encounter/{encounter_id}"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "Encounter",
            "id": "1203252",
            "meta": {
                "versionId": "1",
                "lastUpdated": "2022-04-11T08:37:02.069+00:00",
                "source": "#E5TFiaSdm813st7p"
            },
            "identifier": [{
                "use": "usual",
                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.3.698084.8",
                "value": "27558"
            }],
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

    # Send and check request
    print(f"\nSending PUT request to {url}. Updating Encounter with ID: {encounter_id}")
    response = requests.put(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Encounter updated successfully.")

    return response.json()


def create_encounter(bearer_token, data=None, base_url="https://ea.api.101gen.ai/add_ehr"):
    url = f"{base_url}/Encounter"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "Encounter",
            "meta": {
                "versionId": "1",
                "lastUpdated": "2022-04-11T08:37:02.069+00:00",
                "source": "#E5TFiaSdm813st7p"
            },
            "identifier": [{
                "use": "usual",
                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.3.698084.8",
                "value": "27558"
            }],
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

    # Send and check request
    print(f"\nSending POST request to {url}. Creating new Encounter")
    response = requests.post(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Encounter created successfully.")

    return response.json()


# =============================================
# MedicationRequest Functions
# =============================================

def get_medication_request_by_patient_id(bearer_token, patient_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/MedicationRequest?patient={patient_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Medication Requests by Patient ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Medication Requests retrieved successfully.")

    return response.json()


def get_medication_request_by_id(bearer_token, medication_request_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/MedicationRequest/{medication_request_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Medication Request by ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Medication Request retrieved successfully.")

    return response.json()


def update_medication_request(bearer_token, medication_request_id, data=None, base_url="https://ea.api.101gen.ai/update_ehr"):
    url = f"{base_url}/MedicationRequest/{medication_request_id}"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
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
                "reference": "Patient/10343",
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

    # Send and check request
    print(f"\nSending PUT request to {url}. Updating Medication Request with ID: {medication_request_id}")
    response = requests.put(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Medication Request updated successfully.")

    return response.json()


def create_medication_request(bearer_token, data=None, base_url="https://ea.api.101gen.ai/add_ehr"):
    url = f"{base_url}/MedicationRequest"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
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
                "reference": "Patient/10343",
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

    # Send and check request
    print(f"\nSending POST request to {url}. Creating new Medication Request")
    response = requests.post(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Medication Request created successfully.")

    return response.json()


# =============================================
# Condition Functions
# =============================================

def get_condition_by_patient_id(bearer_token, patient_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/Condition?patient={patient_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Conditions by Patient ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Conditions retrieved successfully.")

    return response.json()


def get_condition_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/Condition?patient={patient_id}&encounter={encounter_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Conditions by Patient ID and Encounter ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Conditions retrieved successfully.")

    return response.json()


def update_condition(bearer_token, condition_id, data=None, base_url="https://ea.api.101gen.ai/update_ehr"):
    url = f"{base_url}/Condition/{condition_id}"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "Condition",
            "id": condition_id,
            "meta": {
                "versionId": "1",
                "lastUpdated": "2025-01-30T16:49:12.937+00:00"
            },
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
            }
        }

    # Send and check request
    print(f"\nSending PUT request to {url}. Updating Condition with ID: {condition_id}")
    response = requests.put(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Condition updated successfully.")

    return response.json()


def create_condition(bearer_token, data=None, base_url="https://ea.api.101gen.ai/add_ehr"):
    url = f"{base_url}/Condition"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "Condition",
            "meta": {
                "versionId": "1",
                "lastUpdated": "2025-01-30T16:49:12.937+00:00"
            },
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
            }
        }

    # Send and check request
    print(f"\nSending POST request to {url}. Creating new Condition")
    response = requests.post(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Condition created successfully.")

    return response.json()


# =============================================
# Observation Functions
# =============================================

def get_observation_by_id(bearer_token, observation_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/Observation/{observation_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Observation by Observation ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Observation retrieved successfully.")

    return response.json()


def get_observation_by_patient_id(bearer_token, patient_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/Observation?patient={patient_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Observations by Patient ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Observations retrieved successfully.")

    return response.json()


def get_observation_by_patient_id_and_encounter_id(bearer_token, patient_id, encounter_id, base_url="https://ea.api.101gen.ai/ehr"):
    url = f"{base_url}/Observation?patient={patient_id}&encounter={encounter_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    response = requests.get(url, headers=headers)
    
    print("Getting Observations by Patient ID and Encounter ID...")
    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Observations retrieved successfully.")

    return response.json()


def update_observation(bearer_token, observation_id, data=None, base_url="https://ea.api.101gen.ai/update_ehr"):
    url = f"{base_url}/Observation/{observation_id}"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
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
                "reference": "Patient/10343",
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

    # Send and check request
    print(f"\nSending PUT request to {url}. Updating Observation with ID: {observation_id}")
    response = requests.put(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Observation updated successfully.")

    return response.json()


def create_observation(bearer_token, data=None, base_url="https://ea.api.101gen.ai/add_ehr"):
    url = f"{base_url}/Observation"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "Observation",
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
                "reference": "Patient/10343",
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

    # Send and check request
    print(f"\nSending POST request to {url}. Creating new Observation")
    response = requests.post(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Observation created successfully.")

    return response.json()


def create_binary(bearer_token, data=None, base_url="https://ea.api.101gen.ai/add_ehr"):
    url = f"{base_url}/Binary"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}
    # Default payload if none provided
    if data is None:
        data = {
            "resourceType": "Binary",
            "contentType": "text/plain",
            "data": "SGVsbG8sIHRoaXMgaXMgYSBzYW1wbGUgdGV4dCBmaWxlLg=="  # Base64 encoded PDF data
        }

    # Send and check request
    print(f"\nSending POST request to {url}. Creating new Binary")
    response = requests.post(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Binary created successfully.")

    return response.json()


def create_order_test(bearer_token, data=None, base_url="https://ea.api.101gen.ai/add_ehr"):
    url = f"{base_url}/ServiceRequest"
    headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    print(data)
    # Default payload if none provided
    if data is None:
        data = {
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

    # Send and check request
    print(f"\nSending POST request to {url}. Creating new Order Test")
    response = requests.post(url, json=data, headers=headers)

    assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
    assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

    print("Order Test created successfully.")

    return response.json()


