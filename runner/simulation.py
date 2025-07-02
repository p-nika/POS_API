# from typing import Dict, List
#
# from core.cashier import Cashier
# from core.customer import Customer
# from core.products import (
#     BasicCart,
#     BasicItemFactory,
#     BasicStorage,
#     ProductIterator,
#     StoreItem,
# )
# from core.receipt import BasicReceiptBase
# from core.repository import DataBaseUtilities, Repository
# from runner.simulation_chain import (
#     CloseReceipt,
#     CustomerArrivingHandler,
#     CustomerPay,
#     FinishSimulation,
#     OpeningReceiptHandler,
#     PrintReceipt,
#     RegisterAllItems,
#     XReport,
#     ZReport,
# )
# from core.store import CashDesks, Store, StoreManager
# from core.wallet import BasicMoneySource, BasicWallet, PaymentMethod
#
#
# class Simulator:
#     _repository: Repository
#     _storage: BasicStorage
#     _receipt_storage: BasicReceiptBase
#     _receipt_base: BasicReceiptBase
#     _cashier: Cashier
#     _customer: Customer
#     _cash_desks: CashDesks
#     _store_manager: StoreManager
#     _store: Store
#     _random_factory: BasicItemFactory
#
#     def __init__(self) -> None:
#         self._repository = DataBaseUtilities("POS.db")
#
#     def create_storage(self) -> None:
#         iterator: ProductIterator = self._repository.get_all_items()
#         items: Dict[StoreItem, int] = {}
#         while iterator.has_next():
#             items[iterator.next_item()] = 9999
#         storage: BasicStorage = BasicStorage(items)
#         self._storage = storage
#
#     def create_receipt_storage(self) -> None:
#         self._receipt_storage = BasicReceiptBase([])
#
#     def create_cashier(self) -> None:
#         self._cashier = Cashier()
#
#     def create_customer(self) -> None:
#         cart: BasicCart = BasicCart([])
#         cash: BasicMoneySource = BasicMoneySource(99999999999999)
#         card: BasicMoneySource = BasicMoneySource(99999999999999)
#         cash_wallet: BasicWallet = BasicWallet(cash)
#         card_wallet: BasicWallet = BasicWallet(card)
#         owned_items: BasicCart = BasicCart([])
#         self._customer = Customer(cart, cash_wallet, card_wallet, owned_items)
#
#     def create_cash_desks(self) -> None:
#         self._cash_desks = CashDesks([self._cashier], self._receipt_storage)
#
#     def create_receipt_base(self) -> None:
#         self._receipt_base = BasicReceiptBase([])
#
#     def create_store_manager(self) -> None:
#         self._store_manager = StoreManager(self._repository)
#
#     def create_store(self) -> None:
#         cash_payment_index: int = 0
#         card_payment_index: int = 0
#         payment_methods: List[PaymentMethod] = self._repository.get_payment_methods()
#         for ind in range(len(payment_methods)):
#             if payment_methods[ind].get_payment_type() == "cash":
#                 cash_payment_index = ind
#             elif payment_methods[ind].get_payment_type() == "card":
#                 card_payment_index = ind
#         cash_payment: PaymentMethod = payment_methods[cash_payment_index]
#         card_payment: PaymentMethod = payment_methods[card_payment_index]
#         self._store = Store(
#             self._cash_desks,
#             self._storage,
#             self._receipt_base,
#             self._store_manager,
#             cash_payment,
#             card_payment,
#         )
#
#     def create_random_factory(self) -> None:
#         self._random_factory = BasicItemFactory(self._storage)
#
#     def simulate(self) -> None:
#         self.create_storage()
#         self.create_receipt_storage()
#         self.create_cashier()
#         self.create_customer()
#         self.create_cash_desks()
#         self.create_receipt_base()
#         self.create_store_manager()
#         self.create_store()
#         self.create_random_factory()
#         for i in range(0, 500):
#             if self._store.get_shift_count() == 3:
#                 break
#             finish_simulation: FinishSimulation = FinishSimulation(self._store)
#             z_report: ZReport = ZReport(
#                 finish_simulation, self._store_manager, self._store
#             )
#             x_report: XReport = XReport(z_report, self._store_manager, self._store)
#             close_receipt: CloseReceipt = CloseReceipt(
#                 x_report,
#                 self._cashier,
#                 self._customer,
#                 self._repository,
#                 self._store.get_shift_count(),
#             )
#             customer_pay: CustomerPay = CustomerPay(
#                 close_receipt, self._cashier, self._customer, self._store
#             )
#             print_receipt: PrintReceipt = PrintReceipt(
#                 customer_pay, self._cashier, self._customer
#             )
#             register_items: RegisterAllItems = RegisterAllItems(
#                 print_receipt, self._cashier, self._customer
#             )
#             opening_receipt: OpeningReceiptHandler = OpeningReceiptHandler(
#                 register_items, self._cashier, self._customer
#             )
#             customer_arriving: CustomerArrivingHandler = CustomerArrivingHandler(
#                 opening_receipt, self._random_factory, self._customer
#             )
#             customer_arriving.execute()
#
#     def make_final_report(self) -> None:
#         # self._store_manager.make_final_report()
#         from displayers import XReportDisplayer
#
#         XReportDisplayer().print_report(
#             self._repository.get_all_time_sales(),
#             self._repository.get_all_time_revenue("cash"),
#             self._repository.get_all_time_revenue("card"),
#         )
#
#
# #
# #
# # simulator: Simulator = Simulator()
# # simulator.simulate()
