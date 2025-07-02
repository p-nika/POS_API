from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from core.products import ItemsRepository
from core.receipt import ReceiptsRepository
from core.units_repository import UnitsRepository


def get_items_repository(request: Request) -> ItemsRepository:
    return request.app.state.items  # type: ignore


def get_units_repository(request: Request) -> UnitsRepository:
    return request.app.state.units  # type: ignore


def get_receipt_repository(request: Request) -> ReceiptsRepository:
    return request.app.state.receipts  # type: ignore


ItemsRepositoryDependable = Annotated[ItemsRepository, Depends(get_items_repository)]
UnitsRepositoryDependable = Annotated[UnitsRepository, Depends(get_units_repository)]
ReceiptRepositoryDependable = Annotated[
    ReceiptsRepository, Depends(get_receipt_repository)
]
