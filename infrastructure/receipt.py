import uuid
from typing import Dict, List
from uuid import UUID

from core.products import ProductIterator, StoreItem
from core.receipt import Receipt, ReceiptIterator
from infrastructure.products import BasicCart


class BasicReceipt(Receipt):
    _id: UUID
    _status: str
    _items: Dict[UUID, StoreItem]
    _items_quantities: Dict[UUID, int]
    _payment_method: str
    _is_paid: bool
    _is_closed: bool

    def __init__(self, receipt_id: UUID = uuid.uuid4(), status: str = "open") -> None:
        self._items = {}
        self._items_quantities = {}
        self._is_paid = False
        self._is_closed = False
        self._id = receipt_id
        self._status = status

    def add_item(self, item: StoreItem, quantity: int) -> None:
        if item.get_id() not in self._items:
            self._items[item.get_id()] = item
            self._items_quantities[item.get_id()] = quantity
        else:
            self._items[item.get_id()] = item
            self._items_quantities[item.get_id()] = (
                self._items_quantities[item.get_id()] + quantity
            )

    def get_items(self) -> ProductIterator:
        all_items: List[StoreItem] = []
        for item in self._items.values():
            all_items.append(item)
        return BasicCart(all_items)

    def get_total_cost(self) -> float:
        result: float = 0
        for item in self._items.values():
            result += item.get_price() * self._items_quantities[item.get_id()]
        return result

    def change_status(self, new_status: str) -> None:
        self._status = new_status

    def get_id(self) -> UUID:
        return self._id

    def get_status(self) -> str:
        return self._status

    def is_closed(self) -> bool:
        return self._is_closed

    def get_item_quantity(self, product_id: UUID) -> int:
        return self._items_quantities[product_id]


class BasicReceiptIterator(ReceiptIterator):
    _receipts: List[Receipt]
    _current_index: int

    def __init__(self, receipts: List[Receipt]):
        self._receipts = receipts
        self._current_index = 0

    def next_receipt(self) -> Receipt:
        result: Receipt = self._receipts[self._current_index]
        self._current_index += 1
        return result

    def has_next(self) -> bool:
        return len(self._receipts) > self._current_index
