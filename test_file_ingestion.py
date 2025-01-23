# test_file_ingestion.py

import pytest
import requests
import yaml

from utils import get_bearer_token, get_file_dataset_id, upload_file, delete_file

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
def test_file_upload(get_bearer_token, project_id="e4cc55c9-305d-478f-b285-96d436229fba"):
	upload_file(get_bearer_token, project_id)

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
def test_delete_file(get_bearer_token, file_dataset_id="", project_id="e4cc55c9-305d-478f-b285-96d436229fba"):
	file_dataset_id = get_file_dataset_id(get_bearer_token, filename="Public Beta Launch Test Cases - requirements import structure.pdf", project_id="e4cc55c9-305d-478f-b285-96d436229fba")
	delete_file(get_bearer_token, file_dataset_id, project_id="e4cc55c9-305d-478f-b285-96d436229fba")
