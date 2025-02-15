# test_smoke_api.py

import pytest
import time
import os

from pytest_check import check
from utils import get_bearer_token
from core_functions import create_agent_api, upload_file_api, upload_url_api, query_agent_api, delete_agent_api


@pytest.fixture(scope="session")
def shared_data():
    data = {}  # Dictionary to store values
    return data

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "https://ea.api.101gen.ai/login",
            "client_side": False,
            "username": "qa_mid_username",
            "password": "qa_mid_password",
        }
    ],
    indirect=True
)
def test_create_agent(get_bearer_token, shared_data, name="Test agent"):
	copilot_id = create_agent_api(get_bearer_token, "ea", "d101d9e4-ce1d-41c9-9ef7-001f0673a4a1")
	shared_data['copilot_id'] = copilot_id

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "https://ea.api.101gen.ai/login",
            "client_side": False,
            "username": "qa_mid_username",
            "password": "qa_mid_password",
        }
    ],
    indirect=True
)
def test_upload_doc(get_bearer_token, shared_data, filepath="/var/lib/jenkins/workspace/Public Beta Launch Test Cases - requirements import structure.pdf"):
	upload_file_api(get_bearer_token, shared_data['copilot_id'], "ea", filepath)
	
@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "https://ea.api.101gen.ai/login",
            "client_side": False,
            "username": "qa_mid_username",
            "password": "qa_mid_password",
        }
    ],
    indirect=True
)
def test_upload_url(get_bearer_token, shared_data):
	upload_url_api(get_bearer_token, shared_data['copilot_id'], "ea", "https://101gen.ai")

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "https://ea.api.101gen.ai/login",
            "client_side": False,
            "username": "qa_mid_username",
            "password": "qa_mid_password",
        }
    ],
    indirect=True
)
def test_query_agent(get_bearer_token, shared_data):
	query_agent_api(get_bearer_token, shared_data['copilot_id'], "ea")

@pytest.mark.parametrize(
    "get_bearer_token",
    [
        {
            "url": "https://ea.api.101gen.ai/login",
            "client_side": False,
            "username": "qa_mid_username",
            "password": "qa_mid_password",
        }
    ],
    indirect=True
)
def test_delete_agent(get_bearer_token, shared_data):
	delete_agent_api(get_bearer_token, shared_data['copilot_id'], "ea")