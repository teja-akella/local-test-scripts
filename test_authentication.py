# test_authentication.py

import pytest
import requests
import yaml

from pytest_check import check

def test_authentication():
	with open('credentials.yaml', 'r') as file:
		creds = yaml.safe_load(file)
	# Bearer Token Request
	# URL and headers 
	url = "https://beta.api.101gen.ai/client/token"
	headers = {
		"content-type": "application/json"
	}

	# Payload
	data = {
		"client_id": creds['client_id'],
		"client_secret": creds["client_secret"]
	}

	# Send and check request
	print("\n\nSending bearer token request...")
	response = requests.post(url, json=data, headers=headers)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print(f"Status Code: {response.status_code}")

	bearer_token = response.json()['access_token']

	# POST Request to chat with Bearer Token
	# URL and headers
	url = "https://beta.api.101gen.ai/chat"

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {bearer_token}"
	}

	# Payload
	data = {
		"query": "What is the best way to avoid back issues due to prolonged periods of sitting?",
		"end_user_id": "e2ffd6b5-0986-4449-8897-3fbced0036b3",
		#"customer_id": "{{TEST_CUSTOMER_ID}}",
		"project_id": "22173081-d3e6-4175-a162-0a94f2c18424",
		"interaction_id": "361ad546-8487-4532-9e25-e00f8a1f8841"
	}

	# Send and check request
	print("\nSending POST request to https://beta.api.101gen.ai/chat")
	print("Query: What is the best way to avoid back issues due to prolonged periods of sitting?")
	response = requests.post(url, json=data, headers=headers)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print(f"\n{response.json()['response_text']}")
