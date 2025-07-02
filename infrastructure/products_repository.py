from sqlite3 import Cursor
from typing import List
from uuid import UUID

from core.products import ItemsRepository, ProductIterator, StoreItem
from core.products_errors import BarcodeExistsError, ItemNotExistsError
from core.units_repository import UnitsRepository
from infrastructure.database_handler import ConnectionHandler
from infrastructure.products import BasicCart, Product


class ItemsInBase(ItemsRepository):
    _handler: ConnectionHandler
    _units_repository: UnitsRepository

    def __init__(self, connection_handler: ConnectionHandler, units: UnitsRepository):
        self._units_repository = units
        self._handler = connection_handler
        self._handler.create_connection()

    @staticmethod
    def create_item(row: List[str]) -> StoreItem:
        return Product(row[2], float(row[4]), UUID(row[1]), row[3], UUID(row[0]))

    def assert_unique_barcode(self, item: StoreItem) -> bool:
        cursor: Cursor = self._handler.get_cursor()
        get_product_query: str = (
            f"SELECT * FROM items WHERE barcode = '{item.get_barcode()}'"
        )
        cursor.execute(get_product_query)
        result: List[str] = cursor.fetchone()
        if result is not None:
            raise BarcodeExistsError(item.get_barcode())
        else:
            return True

    def assert_item_exists(self, product_id: UUID) -> bool:
        cursor: Cursor = self._handler.get_cursor()
        get_product_query: str = f"SELECT * FROM items WHERE id = '{product_id}'"
        cursor.execute(get_product_query)
        result: List[str] = cursor.fetchone()
        if result is None:
            raise ItemNotExistsError(product_id)
        else:
            return False

    def add_product(self, item: StoreItem) -> None:
        self.assert_unique_barcode(item)
        self._units_repository.assert_unit_exists(item.get_unit_id())
        cursor: Cursor = self._handler.get_cursor()
        product_insert_query: str = (
            f"INSERT INTO items (id, unit_id, name, barcode, price) VALUES ("
            f"'{item.get_id()}','{item.get_unit_id()}', '{item.get_name()}', "
            f"'{item.get_barcode()}', {item.get_price()})"
        )
        cursor.execute(product_insert_query)
        self._handler.commit_connection()

    def get_product(self, product_id: UUID) -> StoreItem:
        self.assert_item_exists(product_id)
        cursor: Cursor = self._handler.get_cursor()
        get_product_query: str = f"SELECT * FROM items WHERE id = '{product_id}'"
        cursor.execute(get_product_query)
        result: List[str] = cursor.fetchone()
        return self.create_item(result)

    def get_all_products(self) -> ProductIterator:
        cursor: Cursor = self._handler.get_cursor()
        get_product_query: str = "SELECT * FROM items"
        cursor.execute(get_product_query)
        result: List[List[str]] = cursor.fetchall()
        all_products: List[StoreItem] = []
        for row in result:
            all_products.append(self.create_item(row))
        return BasicCart(all_products)

    def update_price(self, product_id: UUID, new_price: float) -> None:
        self.assert_item_exists(product_id)
        cursor: Cursor = self._handler.get_cursor()
        update_price_query: str = (
            f"UPDATE items SET price = {new_price} WHERE id = '{product_id}'"
        )
        cursor.execute(update_price_query)
        self._handler.commit_connection()
