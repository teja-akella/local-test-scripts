# core_functions.py

import time
import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder
from pytest_check import check

def create_agent_api(bearer_token, platform="ea", org_id="d101d9e4-ce1d-41c9-9ef7-001f0673a4a1", message=""):
	'''
	Create an agent using an API call.

	Parameters:
	bearer_token: authentication token
	platform: string specifying which platform agent will be made on (beta, test, ea)
	org_id: id for organization the agent will be generated in
	message: agent description

	(TODO) Returns:
	project_id: id to specify agent
	response_code: API response code
	'''
	if message == "":
		message = "You are an expert on musculoskeletal (MSK) issues, physiotherapy techniques and yoga exercises, having a conversation with a human patient. answer their queries about MSK issues and exercises and yoga that will help their pain."
	
	url = "https://"+platform+".api.101gen.ai/buildCopilot/chat"

	headers = {
		"Content-Type": "multipart/form-data",
		"Authorization": f"Bearer {bearer_token}"
	}

	# Payload
	multipart_data = MultipartEncoder(
		fields={
		    "org_id": org_id,
	   		"message": message
		}
	)

	headers['Content-Type'] = multipart_data.content_type

	print("Creating new AI Agent..")
	response = requests.post(url, headers=headers, data=multipart_data)

	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	
	print("Agent initialized! The next step is getting the summary.")
	conversation_id = response.json()['conversation_id']

	url = "https://"+platform+".api.101gen.ai/buildCopilot/summary"

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {bearer_token}"
	}

	data = {
		"org_id": org_id,
		"conversation_id": conversation_id
	}

	print("Getting summary...")
	response = requests.post(url, headers=headers, json=data)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

	print("Summary received, the next step is saving the agent.")

	r = response.json()
	description = r['description']
	skill = r['skill'][0]
	audience = r['audience'][0]
	domain = r['domain'][0]
	intent = r['intent'][0]
	dos = r['dos']
	donts = r['donts']
	sample_queries = r['sample_queries'][0]

	url = "https://"+platform+".api.101gen.ai/buildCopilot/save"

	headers = {
		"Content-Type": "multipart/form-data",
		"Authorization": f"Bearer {bearer_token}"
	}

	# Payload
	multipart_data = MultipartEncoder(
		fields={
		    "description": description,
		    "skill": skill,
		    "audience": audience,
		    "domain": domain,
		    "intent": intent,
		    "dos": dos,
		    "donts": donts,
		    "sample_queries": sample_queries,
		    "name": "test copilot api",
		    "profile_pic_url": "https://101genai-public-avtar.s3.amazonaws.com/profile_pic/1.png",
		    "conversation_id": conversation_id,
		    "org_id": org_id
		}
	)

	headers['Content-Type'] = multipart_data.content_type

	print("Saving AI Agent..")
	response = requests.post(url, headers=headers, data=multipart_data)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

	print("AI Agent saved!")
	return response.json()['copilot_id']


def upload_file_api(bearer_token, copilot_id,  platform="ea", filepath="/var/lib/jenkins/workspace/Public Beta Launch Test Cases - requirements import structure.pdf"):
	'''
	Upload a file to a agent using an API call.

	Parameters:
	bearer_token: authentication token
	copilot_id: copilot identifier
	platform: string specifying which platform agent will be made on (beta, test, ea)
	filepath: filepath for document

	(TODO) Returns:
	response_code: API response code
	'''
	project_id = copilot_id

	url = "https://"+platform+".api.101gen.ai/copilots/"+project_id+"/datasets"

	headers = {
		"Authorization": f"Bearer {bearer_token}"
	}

	# Payload
	upload_file_path = filepath

	files= {
    	"files": open(upload_file_path, "rb")
	}

	# Send POST request
	print("\nSending POST request to "+url)

	start_time = time.time()
	response = requests.post(url, headers=headers, files=files)
	end_time = time.time()
	duration = end_time - start_time
	print(f"Upload File API Response Time: {duration:.2f} seconds")
	# print("URL: "+url)
	# print("Headers: "+str(response.request.headers))
	# print("Files: "+str(files))

	check.less(duration, 10, "Uploading file took longer than 10 seconds.")

	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print("Upload successful!")

def upload_url_api(bearer_token, copilot_id, platform="ea", upload_url="https://101gen.ai"):
	'''
	Upload a URL to a agent using an API call.

	Parameters:
	bearer_token: authentication token
	copilot_id: copilot identifier
	platform: string specifying which platform agent will be made on (beta, test, ea)
	upload_url: URL to upload

	(TODO) Returns:
	response_code: API response code
	'''
	project_id = copilot_id

	url = "https://"+platform+".api.101gen.ai/copilots/"+project_id+"/datasets"

	headers = {
		"Content-Type": "multipart/form-data",
		"Authorization": f"Bearer {bearer_token}"
	}

	multipart_data = MultipartEncoder(
		fields={
			"website": upload_url,
			"parse_sub_urls": "1"
		}
	)

	headers['Content-Type'] = multipart_data.content_type

	print("Uploading URL to AI Agent...")
	response = requests.post(url, headers=headers, data=multipart_data)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print("Upload successful!")

def query_agent_api(bearer_token, copilot_id, platform="ea", query="What is a good exercise for MSK pain?", end_user_id="QA MidAcc"):
	'''
	Send a query to a agent using an API call.

	Parameters:
	bearer_token: authentication token
	copilot_id: copilot identifier
	platform: string specifying which platform agent will be made on (beta, test, ea)
	query: query to be made
	end_user_id: name of user posting the query

	(TODO) Returns:
	response_text: text body of agent response
	response_code: API response code
	'''

	project_id = copilot_id
	url = "https://"+platform+".api.101gen.ai/copilots/"+project_id+"/preview"

	headers = {
		"Content-Type": "multipart/form-data",
		"Authorization": f"Bearer {bearer_token}"
	}

	# Payload
	multipart_data = MultipartEncoder(
		fields={
			"query": query,
			"end_user_id": end_user_id
		}
	)

	headers['Content-Type'] = multipart_data.content_type

	# Send and check request
	print("\nSending query to "+url+", project_id: "+project_id)
	print("Query: "+query)
	response = requests.post(url, data=multipart_data, headers=headers)
	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")

	return response.json()['output_text']

def delete_agent_api(bearer_token, copilot_id, platform="ea"):
	'''
	Delete an agent using an API call.

	Parameters:
	bearer_token: authentication token
	copilot_id: copilot identifier
	platform: string specifying which platform agent will be made on (beta, test, ea)
	
	(TODO) Returns:
	response_code: API response code
	'''

	project_id = copilot_id
	url = "https://"+platform+".api.101gen.ai/copilots/"+project_id

	headers = {
		"Authorization": f"Bearer {bearer_token}"
	}

	print("\nSending DELETE request to "+url)

	response = requests.delete(url, headers=headers)

	assert not 400 <= response.status_code <= 499, (f"Client error: {response.status_code} - {response.text}")
	assert not 500 <= response.status_code <= 599, (f"Server error: {response.status_code} - {response.text}")
	print("Agent deleted.")

