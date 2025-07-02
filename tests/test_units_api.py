import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    os.environ["database_path"] = "test"
    return TestClient(init_app())


def test_create_unit(client: TestClient) -> None:
    response = client.post("/units", json={"name": "TestUnit"})
    assert response.status_code == 201
    assert response.json()["unit"]["name"] == "TestUnit"


def test_get_unit(client: TestClient) -> None:
    response = client.get(f"/units/{uuid4()}")
    assert response.status_code == 404
    assert "does not exist" in response.json()["message"].lower()


def test_get_all_units(client: TestClient) -> None:
    response = client.get("/units")
    assert response.status_code == 200
    assert "units" in response.json()


def test_unit_exists(client: TestClient) -> None:
    response = client.post("/units", json={"name": "TestUnit"})
    assert response.status_code == 201
    assert response.json()["unit"]["name"] == "TestUnit"

    response = client.post("/units", json={"name": "TestUnit"})
    assert response.status_code == 409
    assert "already exists" in response.json()["message"].lower()
