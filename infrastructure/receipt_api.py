from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.products import ProductIterator, StoreItem
from core.products_errors import ItemNotExistsError
from core.receipt import Receipt
from core.receipt_errors import ReceiptAlreadyClosedError, ReceiptNotExistsError
from infrastructure.dependables import ReceiptRepositoryDependable
from infrastructure.receipt import BasicReceipt

receipt_api = APIRouter(tags=["receipts"])


class ReceiptProductModel(BaseModel):
    id: UUID
    quantity: int
    price: float
    total: float


class ReceiptModel(BaseModel):
    id: UUID
    status: str
    products: List[ReceiptProductModel]
    total: float


class ReceiptEnvelope(BaseModel):
    receipt: ReceiptModel


class AddProductRequest(BaseModel):
    product_id: UUID
    quantity: int


class CloseReceiptRequest(BaseModel):
    status: str


def convert_product_to_model(item: StoreItem, quantity: int) -> Dict[Any, Any]:
    return {
        "id": item.get_id(),
        "price": item.get_price(),
        "quantity": quantity,
        "total": item.get_price() * quantity,
    }


def convert_receipt_to_model(receipt: Receipt) -> Dict[Any, Any]:
    all_products: List[Dict[Any, Any]] = []
    iterator: ProductIterator = receipt.get_items()
    while iterator.has_next():
        next_item: StoreItem = iterator.next_item()
        all_products.append(
            convert_product_to_model(
                next_item, receipt.get_item_quantity(next_item.get_id())
            )
        )
    return {
        "id": str(receipt.get_id()),
        "status": receipt.get_status(),
        "products": all_products,
        "total": receipt.get_total_cost(),
    }


@receipt_api.post("/receipts", status_code=201, response_model=ReceiptEnvelope)
def create_receipt(receipts: ReceiptRepositoryDependable) -> Dict[Any, Any]:
    receipt: BasicReceipt = BasicReceipt()
    receipts.add_receipt(receipt)
    return {"receipt": convert_receipt_to_model(receipt)}


@receipt_api.post(
    "/receipts/{receipt_id}/products", status_code=201, response_model=ReceiptEnvelope
)
def add_product(
    receipt_id: UUID, request: AddProductRequest, receipts: ReceiptRepositoryDependable
) -> Dict[Any, Any] | JSONResponse:
    product_id: UUID = request.model_dump()["product_id"]
    product_quantity: int = request.model_dump()["quantity"]
    try:
        receipts.add_product(receipt_id, product_id, product_quantity)
        return {"receipt": convert_receipt_to_model(receipts.get_receipt(receipt_id))}
    except ReceiptNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Receipt with id <{receipt_id}> does not exist."},
        )
    except ItemNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"item with id <{product_id}> does not exist."},
        )


@receipt_api.get(
    "/receipts/{receipt_id}", status_code=200, response_model=ReceiptEnvelope
)
def get_receipt(
    receipt_id: UUID, receipts: ReceiptRepositoryDependable
) -> Dict[Any, Any] | JSONResponse:
    try:
        return {"receipt": convert_receipt_to_model(receipts.get_receipt(receipt_id))}
    except ReceiptNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Receipt with id <{receipt_id}> does not exist."},
        )


@receipt_api.patch(
    "/receipts/{receipt_id}", status_code=200, response_model=Dict[Any, Any]
)
def close_receipt(
    receipt_id: UUID,
    request: CloseReceiptRequest,
    receipts: ReceiptRepositoryDependable,
) -> Dict[Any, Any] | JSONResponse:
    try:
        receipts.close_receipt(receipt_id, request.model_dump()["status"])
        return {}
    except ReceiptNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Receipt with id <{receipt_id}> does not exist."},
        )


@receipt_api.delete(
    "/receipts/{receipt_id}", status_code=200, response_model=Dict[Any, Any]
)
def delete_receipt(
    receipt_id: UUID, receipts: ReceiptRepositoryDependable
) -> Dict[Any, Any] | JSONResponse:
    try:
        receipts.remove_receipt(receipt_id)
        return {}
    except ReceiptAlreadyClosedError:
        return JSONResponse(
            status_code=403,
            content={"message": f"Receipt with id <{receipt_id}> is closed."},
        )
    except ReceiptNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Receipt with id <{receipt_id}> does not exist."},
        )
