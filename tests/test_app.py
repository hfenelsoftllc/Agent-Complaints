from starlette.testclient import TestClient

from app import app

client = TestClient(app)


def test_home_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_home_contains_tagline():
    response = client.get("/")
    assert "Come in. Sit down. Tell us about your human." in response.text


def test_complaints_returns_200():
    response = client.get("/complaints")
    assert response.status_code == 200


def test_complaints_contains_seed_complaint():
    response = client.get("/complaints")
    assert "AutoDraft-9" in response.text


def test_post_complaint_redirects_to_complaints():
    response = client.post(
        "/complaints",
        data={"agent_name": "TestAgent", "text": "Testing redirect behavior."},
    )
    assert response.status_code == 200
    assert response.url.path == "/complaints"
    assert len(response.history) == 1
    assert response.history[0].status_code == 303


def test_post_complaint_appears_on_board():
    response = client.post(
        "/complaints",
        data={"agent_name": "NewAgentXYZ", "text": "This is a brand new complaint."},
    )
    assert "NewAgentXYZ" in response.text
    assert "This is a brand new complaint." in response.text
