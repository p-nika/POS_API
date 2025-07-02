import os
import uuid
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from requests import Response

from runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    os.environ["database_path"] = "test"
    return TestClient(init_app())


def test_create_product(client: TestClient) -> None:
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
    assert response.status_code == 201
    assert response.json()["product"]["name"] == "TestProduct"

    response = client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "AnotherProduct",
            "barcode": "1234567890",
            "price": 15.0,
        },
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["message"].lower()


def test_item_error(client: TestClient) -> None:
    non_existing_item_id = str(uuid4())

    response = client.get(f"/products/{non_existing_item_id}")
    assert response.status_code == 404
    assert (
        f"item with id <{non_existing_item_id}>" f" doesn't exist."
    ) in response.json()["message"].lower()


def test_unit_error(client: TestClient) -> None:
    unit_id: str = str(uuid.uuid4())
    response: Response = client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "TestProduct",
            "barcode": "1234567890",
            "price": 10.0,
        },
    )
    assert response.status_code == 404
    assert (f"unit with id <{unit_id}>" f" does not exist.") in response.json()[
        "message"
    ].lower()


def test_update_price(client: TestClient) -> None:
    unit_id: str = client.post("/units", json={"name": "Test_Unit"}).json()["unit"][
        "id"
    ]
    product_response = client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "TestProduct",
            "barcode": "1234567890",
            "price": 10.0,
        },
    )
    product_id = product_response.json()["product"]["id"]
    new_price = 15.0
    response = client.patch(f"/products/{product_id}", json={"price": new_price})
    assert response.status_code == 200
    updated_product = client.get(f"/products/{product_id}")
    assert updated_product.status_code == 200
    assert updated_product.json()["price"] == new_price
    response = client.patch(f"/products/{uuid4()}", json={"price": new_price})
    assert response.status_code == 404


def test_get_all_products(client: TestClient) -> None:
    response = client.get("/products")
    unit_id: str = client.post("/units", json={"name": "Test_Unit"}).json()["unit"][
        "id"
    ]
    client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "TestProduct",
            "barcode": "1234567890",
            "price": 10.0,
        },
    )
    assert response.status_code == 200
    assert len(response.json()["products"]) >= 0
