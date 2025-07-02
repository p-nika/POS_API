from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from core.receipt import ReceiptIterator
from infrastructure.dependables import ReceiptRepositoryDependable

sales_api = APIRouter(tags=["sales"])


class SalesModel(BaseModel):
    n_receipts: int
    revenue: float


class SalesResponseModel(BaseModel):
    sales: SalesModel


@sales_api.get("/sales", status_code=200, response_model=SalesResponseModel)
def get_sales(receipts: ReceiptRepositoryDependable) -> Dict[Any, Any]:
    iterator: ReceiptIterator = receipts.get_receipts()
    receipt_counter: int = 0
    revenue_counter: float = 0
    while iterator.has_next():
        receipt_counter += 1
        revenue_counter += iterator.next_receipt().get_total_cost()
    return {"sales": {"n_receipts": receipt_counter, "revenue": revenue_counter}}
