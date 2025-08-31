from fastapi.testclient import TestClient
from app.main import app
from openai import OpenAI
import pytest
from app.openai_client import get_client




def test_client_initialization():
    client = get_client()
    assert isinstance(client, OpenAI)

def test_api_connection():
    client = get_client()
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'test' if you can hear me."}
            ],
            temperature=0.7
        )
        assert response.choices[0].message.content is not None
        print(f"API Response: {response.choices[0].message.content}")
    except Exception as e:
        pytest.fail(f"API call failed: {str(e)}")


def test_generate_missing_fields():
    client = TestClient(app)
    r = client.post('/generate/all',json={"resume_text":"short","job_description":"short"})
    assert r.status_code == 400
