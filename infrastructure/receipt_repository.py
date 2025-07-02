from sqlite3 import Cursor
from typing import List
from uuid import UUID

from core.products import ItemsRepository
from core.receipt import Receipt, ReceiptIterator, ReceiptsRepository
from core.receipt_errors import ReceiptAlreadyClosedError, ReceiptNotExistsError
from infrastructure.database_handler import ConnectionHandler
from infrastructure.receipt import BasicReceipt, BasicReceiptIterator


class ReceiptsInBase(ReceiptsRepository):
    _handler: ConnectionHandler
    _items_repository: ItemsRepository

    def __init__(
        self, connection_handler: ConnectionHandler, items_repository: ItemsRepository
    ):
        self._handler = connection_handler
        self._handler.create_connection()
        self._items_repository = items_repository

    def assert_id_exists(self, receipt_id: UUID) -> bool:
        cursor: Cursor = self._handler.get_cursor()
        get_receipt_info_query: str = (
            f"SELECT * FROM receipt_info WHERE id = '{receipt_id}'"
        )
        cursor.execute(get_receipt_info_query)
        result: List[str] = cursor.fetchone()
        if result is None:
            raise ReceiptNotExistsError
        else:
            return True

    def assert_receipt_open(self, receipt_id: UUID) -> bool:
        cursor: Cursor = self._handler.get_cursor()
        get_receipt_info_query: str = (
            f"SELECT * FROM receipt_info WHERE id = '{receipt_id}'"
        )
        cursor.execute(get_receipt_info_query)
        result: List[str] = cursor.fetchone()
        if result[1] != "open":
            raise ReceiptAlreadyClosedError
        else:
            return True

    def add_receipt(self, receipt: Receipt) -> None:
        cursor: Cursor = self._handler.get_cursor()
        add_receipt_query: str = (
            f"INSERT INTO receipt_info (id, status, total) VALUES ("
            f"'{receipt.get_id()}', "
            f"'{receipt.get_status()}',"
            f" {receipt.get_total_cost()})"
        )
        cursor.execute(add_receipt_query)
        self._handler.commit_connection()

    @staticmethod
    def create_receipt(row: List[str]) -> BasicReceipt:
        return BasicReceipt(UUID(row[0]), row[1])

    def get_receipt_info(self, receipt_id: UUID) -> BasicReceipt:
        self.assert_id_exists(receipt_id)
        cursor: Cursor = self._handler.get_cursor()
        get_receipt_info_query: str = (
            f"SELECT * FROM receipt_info WHERE id = '{receipt_id}'"
        )
        cursor.execute(get_receipt_info_query)
        result: List[str] = cursor.fetchone()
        return self.create_receipt(result)

    def fill_receipt_products(self, receipt: BasicReceipt) -> None:
        cursor = self._handler.get_cursor()
        get_receipt_products_query: str = (
            f"SELECT * FROM receipt_products WHERE receipt_id = '{receipt.get_id()}'"
        )
        cursor.execute(get_receipt_products_query)
        all_products: List[List[str]] = cursor.fetchall()
        for row in all_products:
            receipt.add_item(
                self._items_repository.get_product(UUID(row[1])), int(row[2])
            )

    def get_receipts(self) -> ReceiptIterator:
        cursor: Cursor = self._handler.get_cursor()
        get_receipt_info_query: str = "SELECT * FROM receipt_info"
        cursor.execute(get_receipt_info_query)
        receipts: List[List[str]] = cursor.fetchall()
        all_receipts: List[Receipt] = []
        for row in receipts:
            current_receipt: BasicReceipt = self.create_receipt(row)
            self.fill_receipt_products(current_receipt)
            all_receipts.append(current_receipt)
        return BasicReceiptIterator(all_receipts)

    def get_receipt(self, receipt_id: UUID) -> Receipt:
        self.assert_id_exists(receipt_id)
        receipt: BasicReceipt = self.get_receipt_info(receipt_id)
        self.fill_receipt_products(receipt)
        return receipt

    def add_product(self, receipt_id: UUID, product_id: UUID, quantity: int) -> None:
        self.assert_id_exists(receipt_id)
        self._items_repository.assert_item_exists(product_id)
        cursor: Cursor = self._handler.get_cursor()
        add_product_query: str = (
            f"INSERT INTO receipt_products (receipt_id, item_id, quantity) VALUES("
            f"'{receipt_id}', '{product_id}', {quantity})"
        )
        cursor.execute(add_product_query)
        self._handler.commit_connection()

    def close_receipt(self, receipt_id: UUID, status: str) -> None:
        self.assert_id_exists(receipt_id)
        cursor: Cursor = self._handler.get_cursor()
        close_receipt_query: str = (
            f"UPDATE receipt_info SET status = '{status}' WHERE id = '{receipt_id}'"
        )
        cursor.execute(close_receipt_query)
        self._handler.commit_connection()

    def remove_receipt(self, receipt_id: UUID) -> None:
        self.assert_id_exists(receipt_id)
        self.assert_receipt_open(receipt_id)
        cursor: Cursor = self._handler.get_cursor()
        remove_receipt_query: str = (
            f"DELETE FROM receipt_info WHERE id = '{receipt_id}'"
        )
        cursor.execute(remove_receipt_query)
        cursor = self._handler.get_cursor()
        remove_receipt_products_query: str = (
            f"DELETE FROM receipt_products WHERE receipt_id = '{receipt_id}'"
        )
        cursor.execute(remove_receipt_products_query)
        self._handler.commit_connection()
