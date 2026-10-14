"""
Automated tests for the Student Portal Flask application.

Run with:  pytest tests/
"""

import json
import pytest
from app import app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Homepage tests ────────────────────────────────────────────────

def test_homepage_status_code(client):
    """GET / should return HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_homepage_contains_title(client):
    """The homepage HTML should contain 'Student Portal'."""
    response = client.get("/")
    assert b"Student Portal" in response.data


def test_homepage_contains_student_names(client):
    """The homepage should list at least one sample student."""
    response = client.get("/")
    assert b"Alice Johnson" in response.data
    assert b"Computer Science" in response.data


# ── Health endpoint tests ─────────────────────────────────────────

def test_health_status_code(client):
    """GET /health should return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_json_response(client):
    """GET /health should return {"status": "healthy"}."""
    response = client.get("/health")
    data = json.loads(response.data)
    assert data == {"status": "healthy"}


def test_health_content_type(client):
    """GET /health should return application/json."""
    response = client.get("/health")
    assert response.content_type == "application/json"
