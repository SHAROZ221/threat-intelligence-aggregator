import pytest
import sqlite3
import os
from app import app, check_ip_virustotal, check_domain_virustotal


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_export_csv(client):
    response = client.get("/export")
    assert response.status_code == 200
    assert "text/csv" in response.content_type
    assert b"indicator" in response.data


def test_database_connection():
    conn = sqlite3.connect("threats.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM threats")
    count = cursor.fetchone()[0]
    conn.close()
    assert count >= 0