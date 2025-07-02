from typing import Self

import pytest

from core.products import StoreItem
from core.receipt import Receipt, ReceiptIterator
from core.units import Unit
from infrastructure.products import Product
from infrastructure.receipt import BasicReceipt, BasicReceiptIterator


class TestReceiptBuilder:
    _current_receipt: Receipt = BasicReceipt()

    def with_item(
        self,
        item: StoreItem = Product("test item 1", 15, Unit("sample").get_id(), "000"),
        quantity: int = 1,
    ) -> Self:
        self._current_receipt.add_item(item, quantity)
        return self

    def build(self) -> Receipt:
        return self._current_receipt


@pytest.fixture
def receipt_builder() -> TestReceiptBuilder:
    return TestReceiptBuilder()


def test_receipt_fields(receipt_builder: TestReceiptBuilder) -> None:
    receipt: Receipt = receipt_builder.with_item().build()
    assert receipt.get_items().next_item().get_name() == "test item 1"
    assert receipt.get_total_cost() == 15
    assert receipt.get_status() == "open"
    assert not receipt.is_closed()


def test_receipt_status(receipt_builder: TestReceiptBuilder) -> None:
    receipt: Receipt = receipt_builder.build()
    receipt.change_status("closed")
    assert receipt.get_status() == "closed"


def test_receipt_quantity(receipt_builder: TestReceiptBuilder) -> None:
    receipt: Receipt = receipt_builder.with_item().build()
    assert receipt.get_item_quantity(receipt.get_items().next_item().get_id()) == 2


def test_receipt_iterator(receipt_builder: TestReceiptBuilder) -> None:
    receipt: Receipt = receipt_builder.with_item().build()
    iterator: ReceiptIterator = BasicReceiptIterator([receipt])
    assert iterator.has_next()
    assert iterator.next_receipt() == receipt
