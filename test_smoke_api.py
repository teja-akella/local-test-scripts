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
            "url": "http://localhost:5173/login",
            "client_side": False,
            "username": "qa_low_username",
            "password": "qa_low_password",
        }
    ],
    indirect=True
)
def test_create_agent(get_bearer_token, shared_data, name="Test agent"):
	copilot_id = create_agent_api(get_bearer_token,"1e780036-83c2-4134-b63c-639853ae10d3")
	shared_data['copilot_id'] = copilot_id

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
def test_upload_doc(get_bearer_token, shared_data, filepath="/var/lib/jenkins/workspace/Public Beta Launch Test Cases - requirements import structure.pdf"):
	upload_file_api(get_bearer_token, shared_data['copilot_id'], filepath)
	
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
def test_upload_url(get_bearer_token, shared_data):
	upload_url_api(get_bearer_token, shared_data['copilot_id'])

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
def test_query_agent(get_bearer_token, shared_data):
	query_agent_api(get_bearer_token, shared_data['copilot_id'])

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
def test_delete_agent(get_bearer_token, shared_data):
	delete_agent_api(get_bearer_token, shared_data['copilot_id'])