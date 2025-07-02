import os
import sqlite3

from fastapi import FastAPI

from infrastructure.database_handler import ConnectionHandler, DefaultTablesHandler
from infrastructure.products_api import products_api
from infrastructure.products_repository import ItemsInBase
from infrastructure.receipt_api import receipt_api
from infrastructure.receipt_repository import ReceiptsInBase
from infrastructure.sales_api import sales_api
from infrastructure.units_api import units_api
from infrastructure.units_repository import UnitsInBase


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(products_api)
    app.include_router(units_api)
    app.include_router(receipt_api)
    app.include_router(sales_api)
    data_base_path = "pos.db"
    if os.getenv("database_path") == "test":
        connection = sqlite3.connect("testing_pos.db")
        cursor = connection.cursor()
        DefaultTablesHandler.delete_receipt_product(cursor)
        DefaultTablesHandler.delete_receipts_info(cursor)
        DefaultTablesHandler.delete_units(cursor)
        DefaultTablesHandler.delete_items(cursor)
        connection = sqlite3.connect("testing_pos.db")
        cursor = connection.cursor()
        DefaultTablesHandler.create_items(cursor)
        DefaultTablesHandler.create_units(cursor)
        DefaultTablesHandler.create_receipt_info(cursor)
        DefaultTablesHandler.create_receipt_products(cursor)
        data_base_path = "testing_pos.db"
    app.state.units = UnitsInBase(ConnectionHandler(data_base_path))
    app.state.items = ItemsInBase(ConnectionHandler(data_base_path), app.state.units)
    app.state.receipts = ReceiptsInBase(
        ConnectionHandler(data_base_path), app.state.items
    )
    return app
