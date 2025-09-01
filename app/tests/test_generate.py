from fastapi.testclient import TestClient
from app.main import app
from openai import OpenAI
import pytest
from app.openai_client import get_client
import os
from unittest.mock import patch

# Create test client
client = TestClient(app)


def test_client_initialization():
    client = get_client()
    assert isinstance(client, OpenAI)


@pytest.fixture
def mock_openai():
    with patch('app.routers.generate.get_client') as mock:
        # Mock the OpenAI response
        mock.return_value.chat.completions.create.return_value.choices = [
            type('Choice', (), {'message': type(
                'Message', (), {'content': 'mocked response'})()})()
        ]
        yield mock


def test_generate_missing_fields(mock_openai):
    response = client.post(
        "/generate/all",
        json={
            "resume_text": "This is a valid length resume text that meets the minimum requirement of 50 characters for testing purposes.",
            "job_description": "This is a valid length job description that meets the minimum requirement of 50 characters for testing.",
            "tone_hint": "professional"
        }
    )
    assert response.status_code == 200


def test_generate_invalid_length():
    response = client.post(
        "/generate/all",
        json={
            "resume_text": "too short",
            "job_description": "too short",
            "tone_hint": "professional"
        }
    )
    # Changed from 400 to 422 since FastAPI returns 422 for validation errors
    assert response.status_code == 422
