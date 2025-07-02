from typing import Protocol
from uuid import UUID

# class BarcodeFactory(Protocol):
#     @staticmethod
#     def get_barcode() -> str:
#         pass


class StoreItem(Protocol):
    def get_id(self) -> UUID:
        pass

    def get_price(self) -> float:
        pass

    def get_name(self) -> str:
        pass

    def get_barcode(self) -> str:
        pass

    def set_price(self, new_price: float) -> None:
        pass

    def get_unit_id(self) -> UUID:
        pass


# class StoreItemFactory(Protocol):
#     def create_item(self) -> StoreItem:
#         pass


class ProductIterator(Protocol):
    def next_item(self) -> StoreItem:
        pass

    def has_next(self) -> bool:
        pass

    def reset_index(self) -> None:
        pass

    def reset_iterator(self) -> None:
        pass


class CartIterator(ProductIterator):
    def add_item(self, item: StoreItem) -> None:
        pass


# class Storage(Protocol):
#     def has_item(self, item: StoreItem, number: int) -> bool:
#         pass


class ItemsRepository(Protocol):
    def add_product(self, item: StoreItem) -> None:
        pass

    def get_product(self, product_id: UUID) -> StoreItem:
        pass

    def get_all_products(self) -> ProductIterator:
        pass

    def update_price(self, product_id: UUID, new_price: float) -> None:
        pass

    def assert_item_exists(self, product_id: UUID) -> bool:
        pass
