# test_authentication.py

import pytest
import requests
import yaml

from pytest_check import check
from utils import get_bearer_token, send_slack_message

def test_authentication(get_bearer_token):

	try:
		bearer_token = get_bearer_token
	except AssertionError:
		send_slack_message("Bearer Token Request Failed. Please check latest Jenkins run at https://dev.jenkins.101gen.ai/job/Authentication%20Test/")
		assert 0 == 1

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