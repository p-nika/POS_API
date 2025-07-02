import uuid
from typing import List
from uuid import UUID

from core.products import CartIterator, StoreItem

# class BasicBarcodeFactory(BarcodeFactory):
#     static_counter: int = 0
#
#     @staticmethod
#     def get_barcode() -> str:
#         BasicBarcodeFactory.static_counter += 1
#         return str(BasicBarcodeFactory.static_counter).zfill(10)


class Product(StoreItem):
    name: str
    price: float
    barcode: str
    id: UUID
    unit_id: UUID

    def __init__(
        self,
        name: str,
        price: float,
        unit_id: UUID,
        barcode: str,
        product_id: UUID = uuid.uuid4(),
    ):
        self.name = name
        self.price = price
        self.barcode = barcode
        self.id = product_id
        self.unit_id = unit_id

    def get_price(self) -> float:
        return self.price

    def get_name(self) -> str:
        return self.name

    def get_barcode(self) -> str:
        return self.barcode

    def get_id(self) -> UUID:
        return self.id

    def set_price(self, new_price: float) -> None:
        self.price = new_price

    def get_unit_id(self) -> UUID:
        return self.unit_id


class BasicCart(CartIterator):
    _items: List[StoreItem]
    _current_index: int

    def __init__(self, items: List[StoreItem]):
        self._items = items
        self._current_index = 0

    def next_item(self) -> StoreItem:
        result_item: StoreItem = self._items[self._current_index]
        self._current_index += 1
        return result_item

    def has_next(self) -> bool:
        return len(self._items) > self._current_index

    def add_item(self, item: StoreItem) -> None:
        self._items.append(item)

    def reset_index(self) -> None:
        self._current_index = 0

    def reset_iterator(self) -> None:
        self._items = []
        self.reset_index()


# class BasicStorage(Storage):
#     _items: Dict[StoreItem, int]
#
#     def __init__(self, items: Dict[StoreItem, int]):
#         self._items = items
#
#     def has_item(self, item: StoreItem, number: int) -> bool:
#         return self._items[item] >= number
#
#     def get_items(self) -> List[StoreItem]:
#         return list(self._items.keys())
#
#
# class BasicItemFactory(StoreItemFactory):
#     _storage: BasicStorage
#
#     def __init__(self, storage: BasicStorage):
#         self._storage = storage
#
#     def create_item(self) -> StoreItem:
#         items: List[StoreItem] = self._storage.get_items()
#         return items[randint(0, len(items) - 1)]
