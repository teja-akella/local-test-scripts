# utils.py

import pytest
import time
import os
import yaml
import requests
import json

from pytest_check import check
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"


@pytest.fixture(scope="session")
def setup():
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	# chrome_options.add_argument("--headless")  # Run in headless mode
	# chrome_options.add_argument("--disable-gpu")  # Disable GPU usage (usually recommended)
	# chrome_options.add_argument("--window-size=1920,1080")

	# Setup: Initialize the WebDriver and open the browser
	driver = webdriver.Chrome(options=chrome_options)
	driver.maximize_window()
	yield driver
	# Teardown: Close the browser after the test
	driver.quit()

def login(setup):
	driver = setup
	with open('../credentials.yaml', 'r') as file:
		creds = yaml.safe_load(file)

	# Step 1: Navigate to the website
	driver.get("https://test.app.101gen.ai/login")  
	wait = WebDriverWait(driver, timeout=30)
	
	# Step 2: Locate and interact with the form fields
	email_field = driver.find_element(By.XPATH, "//input[@name='username']")  
	password_field = driver.find_element(By.XPATH, "//input[@name='password']")  
	
	# Step 3: Input data into the fields
	email_field.send_keys(creds['qa_mid_username'])
	password_field.send_keys(creds['qa_mid_password'])

	# Step 4: Submit the form
	submit_button = wait.until(
		EC.element_to_be_clickable((By.XPATH, "//span[text()='Login']/.."))
	)
	submit_button.click()
	wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Welcome to 101GenAI!']")))
	assert driver.current_url == "https://test.app.101gen.ai/dashboard", "Did not reach the correct URL."
	time.sleep(5)

def open_copilot(setup, name='Test Copilot'):
	# opens the copilot with the 'name' parameter on the dashboard.
	# this function assumes user is already logged in and at the dashboard.
	driver = setup
	wait = WebDriverWait(driver, timeout=10)
	copilot_xpath = "//h3[text()='"+name+"']/ancestor::div[contains(@class, 'relative')]/following-sibling::div[@class='cursor-pointer']"
	open_copilot = wait.until(
		EC.element_to_be_clickable((By.XPATH, copilot_xpath))
	)
	open_copilot.click()

	wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='Skills']")))
	time.sleep(5)

@pytest.fixture(scope="session")
def get_bearer_token(request):
	params = getattr(request, "param", {})

	url = params.get('url', 'https://beta.api.101gen.ai/client/token')
	client_side = params.get('client_side', True)
	client_id = params.get('client_id', 'beta_101genai_client_id')
	client_secret = params.get('client_secret', 'beta_101genai_client_secret')
	username = params.get('username', 'test_root_username')
	password = params.get('password', 'test_root_password')

	with open('../credentials.yaml', 'r') as file:
		creds = yaml.safe_load(file)
		if client_side:
			data = {
				"client_id": creds[client_id],
				"client_secret": creds[client_secret]
			}
		else:
			data = {
				"username": creds[username],
				"password": creds[password]
			}
	# Bearer Token Request
	# headers 
	headers = {
		"content-type": "application/json"
	}

	print("Request Details:")
	print(f"URL: {url}")
	print(f"Headers: {json.dumps(headers, indent=2)}")
	# Send and check request
	print("\n\nSending bearer token request...")
	response = requests.post(url, json=data, headers=headers)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print(f"Status Code: {response.status_code}")

	if client_side:
		return response.json()['access_token']
	else:	
		return response.json()['token']

def send_slack_message(message):
	"""Send a message to slack via a webhook."""
	payload = {"text": message}
	response = requests.post(SLACK_WEBHOOK_URL, json=payload)

	if response.status_code == 200:
		print("Message sent to Slack successfully.")
	else:
		print(f"Failed to send Slack message. Status Code: {response.status_code}, Response: {response.text}")

def create_and_add_new_user_to_org(get_bearer_token, email="testuser@gmail.com", first_name="TestUser", last_name="API", permission_group="member"):
	with open('../credentials.yaml', 'r') as file:
		creds = yaml.safe_load(file)

	test_org_id = creds['ea_101genai_org_id']
	bearer_token = get_bearer_token

	url = "https://ea.api.101gen.ai/org/user/create"

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {bearer_token}"
	}

	# Payload
	data = {
	    "org_id": test_org_id, 
	    "email": email,
	    "first_name": first_name,
	    "last_name": last_name,
	    "permission_group": permission_group
	}

	print("Creating and adding new user to org..")
	response = requests.post(url, json=data, headers=headers)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print("User created and added!")

def create_new_org(get_bearer_token, name="Test Org 1", domain="test14.com"):
	bearer_token = get_bearer_token

	url = "https://ea.api.101gen.ai/org"

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {bearer_token}"
	}

	# Payload
	data = {
	    "name": name,
		"domain": domain
	}

	print("Creating new org..")
	response = requests.post(url, json=data, headers=headers)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print("Org created!")

def get_file_dataset_id(get_bearer_token, filename="Public Beta Launch Test Cases - requirements import structure.pdf", project_id="e4cc55c9-305d-478f-b285-96d436229fba"):
	bearer_token = get_bearer_token

	url = "https://ea.api.101gen.ai/copilots/"+project_id+"/datasets"

	headers = {
		"Authorization": f"Bearer {bearer_token}"
	}

	response = requests.get(url, headers=headers)
	print("\nSending GET request to "+url)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print("Files received successfully..")
	for i in response.json()['docs']:
		if i['name'] == filename:
			return i['id']
	return None

def delete_file(get_bearer_token, file_dataset_id="", project_id="e4cc55c9-305d-478f-b285-96d436229fba"):
	# upload file

	#time.sleep(5)
	bearer_token = get_bearer_token
	
	url = "https://ea.api.101gen.ai/copilots/"+project_id+"/datasets"

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {bearer_token}"
	}

	if file_dataset_id is None:
		file_dataset_id = get_file_dataset_id(get_bearer_token, filename="Public Beta Launch Test Cases - requirements import structure.pdf", project_id="e4cc55c9-305d-478f-b285-96d436229fba")

	print("file_dataset_id: "+str(file_dataset_id))
	data = {
		"dataset_ids": [file_dataset_id]
	}

	print("\nSending DELETE request to "+url)

	start_time = time.time()
	response = requests.delete(url, headers=headers, json=data)
	end_time = time.time()
	duration = end_time - start_time
	print(f"API Response Time: {duration:.2f} seconds")
	check.less(duration, 10, "Deleting file took longer than 10 seconds.")

	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print("File deleted.")
