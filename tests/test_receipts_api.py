import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from requests import Response

from runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    os.environ["database_path"] = "test"
    return TestClient(init_app())


def test_create_receipt(client: TestClient) -> None:
    response = client.post("/receipts")
    assert response.status_code == 201
    assert "receipt" in response.json()


def test_add_product(client: TestClient) -> None:
    receipt_response = client.post("/receipts")
    receipt_id = receipt_response.json()["receipt"]["id"]
    unit_id: str = client.post("/units", json={"name": "Test_Unit"}).json()["unit"][
        "id"
    ]
    response: Response = client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "TestProduct",
            "barcode": "1234567890",
            "price": 10.0,
        },
    )
    product_id: str = response.json()["product"]["id"]
    response = client.post(
        f"/receipts/{receipt_id}/products",
        json={"product_id": product_id, "quantity": 2},
    )
    assert response.status_code == 201
    assert "receipt" in response.json()
    non_existing_receipt_id = str(uuid4())
    response = client.post(
        f"/receipts/{non_existing_receipt_id}/products",
        json={"product_id": product_id, "quantity": 2},
    )
    assert response.status_code == 404
    assert "does not exist" in response.json()["message"].lower()
    non_existing_product_id = str(uuid4())
    response = client.post(
        f"/receipts/{receipt_id}/products",
        json={"product_id": non_existing_product_id, "quantity": 2},
    )
    assert response.status_code == 404
    assert "does not exist" in response.json()["message"].lower()


def test_get_receipt(client: TestClient) -> None:
    receipt_response = client.post("/receipts")
    receipt_id = receipt_response.json()["receipt"]["id"]
    response = client.get(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    assert "receipt" in response.json()
    non_existing_receipt_id = str(uuid4())
    response = client.get(f"/receipts/{non_existing_receipt_id}")
    assert response.status_code == 404
    assert "does not exist" in response.json()["message"].lower()


def test_close_receipt(client: TestClient) -> None:
    receipt_response = client.post("/receipts")
    receipt_id = receipt_response.json()["receipt"]["id"]
    response = client.patch(f"/receipts/{receipt_id}", json={"status": "closed"})
    assert response.status_code == 200
    closed_receipt = client.get(f"/receipts/{receipt_id}")
    assert closed_receipt.status_code == 200
    assert closed_receipt.json()["receipt"]["status"] == "closed"
    non_existing_receipt_id = str(uuid4())
    response = client.patch(
        f"/receipts/{non_existing_receipt_id}", json={"status": "closed"}
    )
    assert response.status_code == 404
    assert "does not exist" in response.json()["message"].lower()


def test_delete_receipt(client: TestClient) -> None:
    receipt_response = client.post("/receipts")
    receipt_id = receipt_response.json()["receipt"]["id"]
    response = client.delete(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    deleted_receipt = client.get(f"/receipts/{receipt_id}")
    assert deleted_receipt.status_code == 404
    assert "does not exist" in deleted_receipt.json()["message"].lower()
    non_existing_receipt_id = str(uuid4())
    response = client.delete(f"/receipts/{non_existing_receipt_id}")
    assert response.status_code == 404
    assert "does not exist" in response.json()["message"].lower()
