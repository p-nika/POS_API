from random import randint
from typing import List

from core.products import CartIterator, StoreItem
from core.units import Unit
from infrastructure.products import BasicCart, Product


def test_product_fields() -> None:
    random_number: int = randint(0, 100)
    unit: Unit = Unit("sample unit")
    item: StoreItem = Product("test_product", random_number, unit.get_id(), "000")
    assert item.get_name() == "test_product"
    assert item.get_price() == random_number
    assert item.get_unit_id() == unit.get_id()
    assert item.get_barcode() == "000"


def test_set_price() -> None:
    unit: Unit = Unit("sample unit")
    item: StoreItem = Product("test_product", 10, unit.get_id(), "000")
    item.set_price(5)
    assert item.get_price() == 5


def test_cart_iteration() -> None:
    unit: Unit = Unit("sample unit")
    items: List[StoreItem] = [
        Product("test item 1", 10, unit.get_id(), "000"),
        Product("test item 2", 11, unit.get_id(), "001"),
    ]
    cart: CartIterator = BasicCart(items)
    got_items: List[StoreItem] = []
    while cart.has_next():
        got_items.append(cart.next_item())
    assert got_items[0].get_name() == "test item 1"
    assert got_items[1].get_name() == "test item 2"


def test_cart_methods() -> None:
    unit: Unit = Unit("sample unit")
    items: List[StoreItem] = [Product("test item 1", 10, unit.get_id(), "000")]
    cart: CartIterator = BasicCart(items)
    cart.reset_iterator()
    cart.add_item(Product("test item 2", 11, unit.get_id(), "001"))
    cart.reset_index()
    assert cart.next_item().get_name() == "test item 2"
