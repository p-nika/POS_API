import sqlite3
from sqlite3 import Connection, Cursor


class DefaultTablesHandler:
    @staticmethod
    def delete_items(cursor: Cursor) -> None:
        cursor.execute(
            """
                    DROP TABLE IF EXISTS items
                """
        )

    @staticmethod
    def delete_units(cursor: Cursor) -> None:
        cursor.execute(
            """
                        DROP TABLE IF EXISTS units
                    """
        )

    @staticmethod
    def delete_receipts_info(cursor: Cursor) -> None:
        cursor.execute(
            """
                        DROP TABLE IF EXISTS receipt_info
                    """
        )

    @staticmethod
    def delete_receipt_product(cursor: Cursor) -> None:
        cursor.execute(
            """
                        DROP TABLE IF EXISTS receipt_products
                    """
        )

    @staticmethod
    def create_items(cursor: Cursor) -> None:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                unit_id TEXT,
                name TEXT,
                barcode TEXT,
                price FLOAT
            )
        """
        )

    @staticmethod
    def create_units(cursor: Cursor) -> None:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS units (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """
        )

    @staticmethod
    def create_receipt_info(cursor: Cursor) -> None:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS receipt_info (
                id TEXT PRIMARY KEY,
                status TEXT,
                total FLOAT
            )
        """
        )

    @staticmethod
    def create_receipt_products(cursor: Cursor) -> None:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS receipt_products (
                receipt_id TEXT,
                item_id TEXT,
                quantity INTEGER,
                FOREIGN KEY (receipt_id) REFERENCES receipt_info(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """
        )


class ConnectionHandler:
    _data_base_name: str
    _connection: Connection

    def __init__(self, data_base_name: str):
        self._data_base_name = data_base_name

    def create_connection(self) -> None:
        self._connection = sqlite3.connect(
            self._data_base_name, check_same_thread=False
        )

    def get_cursor(self) -> Cursor:
        return self._connection.cursor()

    def commit_connection(self) -> None:
        self._connection.commit()
