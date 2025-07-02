# from typing import Dict, List, Protocol
#
# from core.products import ProductIterator, StoreItem
# from core.receipt import Receipt
# from core.wallet import PaymentMethod
#
#
# class Repository(Protocol):
#     def get_revenue(self, payment_method: str, shift_number: int) -> float:
#         pass
#
#     def get_all_time_revenue(self, payment_method: str) -> float:
#         pass
#
#     def get_items_sales(self, shift_number: int) -> Dict[StoreItem, int]:
#         pass
#
#     def get_all_time_sales(self) -> Dict[StoreItem, int]:
#         pass
#
#     def add_item(self, item: StoreItem) -> None:
#         pass
#
#     def get_all_items(self) -> ProductIterator:
#         pass
#
#     def add_payment_method(self, payment_method: PaymentMethod) -> None:
#         pass
#
#     def get_payment_methods(self) -> List[PaymentMethod]:
#         pass
#
#     def add_receipt(self, receipt: Receipt, shift_number: int) -> None:
#         pass
