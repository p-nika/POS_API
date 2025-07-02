# from random import randint
#
# from cashier import Cashier
# from customer import Customer
# from displayers import BasicReceiptDisplayer
# from products import StoreItemFactory
# from receipt import BasicReceiptFactory
# from repository import Repository
# from store import InteractionHandler, Store, StoreManager
#
#
# class CustomerArrivingHandler(InteractionHandler):
#     _next_handler: InteractionHandler
#     _item_factory: StoreItemFactory
#     _customer: Customer
#
#     def __init__(
#         self,
#         next_handler: InteractionHandler,
#         item_factory: StoreItemFactory,
#         customer: Customer,
#     ):
#         self._next_handler = next_handler
#         self._item_factory = item_factory
#         self._customer = customer
#
#     def execute(self) -> None:
#         # filling customers cart
#         for i in range(10):
#             self._customer.add_item_in_cart(self._item_factory.create_item())
#         self._next_handler.execute()
#         # delegating to the next handler
#
#
# class OpeningReceiptHandler(InteractionHandler):
#     _next_handler: InteractionHandler
#     _cashier: Cashier
#     _customer: Customer
#
#     def __init__(
#         self, next_handler: InteractionHandler, cashier: Cashier, customer: Customer
#     ):
#         self._next_handler = next_handler
#         self._cashier = cashier
#         self._customer = customer
#
#     def execute(self) -> None:
#         new_receipt = BasicReceiptFactory.create_receipt()
#         self._cashier.open_receipt(new_receipt, self._customer.get_cart())
#         self._next_handler.execute()
#
#
# class RegisterAllItems(InteractionHandler):
#     _next_handler: InteractionHandler
#     _cashier: Cashier
#     _customer: Customer
#
#     def __init__(
#         self, next_handler: InteractionHandler, cashier: Cashier, customer: Customer
#     ):
#         self._next_handler = next_handler
#         self._cashier = cashier
#         self._customer = customer
#
#     def execute(self) -> None:
#         while not self._cashier.is_receipt_finished():
#             self._cashier.register_item()
#         self._next_handler.execute()
#
#
# class PrintReceipt(InteractionHandler):
#     _next_handler: InteractionHandler
#     _cashier: Cashier
#     _customer: Customer
#
#     def __init__(
#         self, next_handler: InteractionHandler, cashier: Cashier, customer: Customer
#     ):
#         self._next_handler = next_handler
#         self._cashier = cashier
#         self._customer = customer
#
#     def execute(self) -> None:
#         BasicReceiptDisplayer().print_receipt(self._cashier.get_current_receipt())
#         self._next_handler.execute()
#
#
# class CustomerPay(InteractionHandler):
#     _next_handler: InteractionHandler
#     _cashier: Cashier
#     _customer: Customer
#     _store: Store
#
#     def __init__(
#         self,
#         next_handler: InteractionHandler,
#         cashier: Cashier,
#         customer: Customer,
#         store: Store,
#     ):
#         self._cashier = cashier
#         self._next_handler = next_handler
#         self._customer = customer
#         self._store = store
#
#     def execute(self) -> None:
#         if self._store.get_customer_count() % 2 == 0:
#             self._cashier.get_current_receipt().set_discount(25)
#         if randint(0, 1) == 0:
#             self._cashier.get_current_receipt().set_payment_method(
#                 self._store.get_cash_payment_method().get_payment_type()
#             )
#             self._store.make_cash_payment(
#                 self._customer, self._cashier.get_current_receipt()
#             )
#         else:
#             self._cashier.get_current_receipt().set_payment_method(
#                 self._store.get_card_payment_method().get_payment_type()
#             )
#             self._store.make_card_payment(
#                 self._customer, self._cashier.get_current_receipt()
#             )
#         self._next_handler.execute()
#
#
# class CloseReceipt(InteractionHandler):
#     _next_handler: InteractionHandler
#     _cashier: Cashier
#     _customer: Customer
#     _repository: Repository
#     _shift_number: int
#
#     def __init__(
#         self,
#         next_handler: InteractionHandler,
#         cashier: Cashier,
#         customer: Customer,
#         repository: Repository,
#         shift_number: int,
#     ):
#         self._cashier = cashier
#         self._next_handler = next_handler
#         self._customer = customer
#         self._repository = repository
#         self._shift_number = shift_number
#
#     def execute(self) -> None:
#         self._cashier.close_receipt(self._customer)
#         self._repository.add_receipt(
#             self._cashier.get_current_receipt(), self._shift_number
#         )
#         self._next_handler.execute()
#
#
# class Counter:
#     _counter: int
#
#     def __init__(self) -> None:
#         self._counter = 0
#
#     def increment(self) -> None:
#         self._counter += 1
#
#     def get_count(self) -> int:
#         return self._counter
#
#
# class XReport(InteractionHandler):
#     _next_handler: InteractionHandler
#     _store_manager: StoreManager
#     _store: Store
#
#     def __init__(
#         self,
#         next_handler: InteractionHandler,
#         store_manager: StoreManager,
#         store: Store,
#     ):
#         self._next_handler = next_handler
#         self._store_manager = store_manager
#         self._store = store
#
#     def execute(self) -> None:
#         if (
#             self._store.get_customer_count() > 0
#             and self._store.get_customer_count() % 20 == 0
#         ):
#             response: str = input("do you want to make an X report? y/n ")
#             if response == "y":
#                 self._store_manager.make_xreport(self._store.get_shift_count())
#
#         self._next_handler.execute()
#
#
# class ZReport(InteractionHandler):
#     _next_handler: InteractionHandler
#     _store_manager: StoreManager
#     _store: Store
#
#     def __init__(
#         self,
#         next_handler: InteractionHandler,
#         store_manager: StoreManager,
#         store: Store,
#     ):
#         self._next_handler = next_handler
#         self._store_manager = store_manager
#         self._store = store
#
#     def execute(self) -> None:
#         if (
#             self._store.get_customer_count() > 0
#             and self._store.get_customer_count() % 100 == 0
#         ):
#             response: str = input("do you want to make a Z report? y/n ")
#             if response == "y":
#                 self._store.add_shift_count()
#         self._next_handler.execute()
#
#
# class FinishSimulation(InteractionHandler):
#     _next_handler: InteractionHandler
#     _store: Store
#
#     def __init__(self, store: Store):
#         self._store = store
#
#     def execute(self) -> None:
#         if self._store.get_shift_count() != 3:
#             self._store.add_customer_count()
#             # self._next_handler.execute()
#
#     def set_next(self, next_handler: InteractionHandler) -> None:
#         self._next_handler = next_handler
