from typing import Protocol
from uuid import UUID

from core.products import ProductIterator, StoreItem


class Receipt(Protocol):
    def add_item(self, item: StoreItem, quantity: int) -> None:
        pass

    def get_items(self) -> ProductIterator:
        pass

    def get_total_cost(self) -> float:
        pass

    def change_status(self, new_status: str) -> None:
        pass

    def get_id(self) -> UUID:
        pass

    def get_status(self) -> str:
        pass

    def is_closed(self) -> bool:
        pass

    def get_item_quantity(self, product_id: UUID) -> int:
        pass


class ReceiptIterator(Protocol):
    def next_receipt(self) -> Receipt:
        pass

    def has_next(self) -> bool:
        pass


class ReceiptsRepository(Protocol):
    def add_receipt(self, receipt: Receipt) -> None:
        pass

    def get_receipts(self) -> ReceiptIterator:
        pass

    def add_product(self, receipt_id: UUID, product_id: UUID, quantity: int) -> None:
        pass

    def get_receipt(self, receipt_id: UUID) -> Receipt:
        pass

    def close_receipt(self, receipt_id: UUID, status: str) -> None:
        pass

    def remove_receipt(self, receipt_id: UUID) -> None:
        pass
