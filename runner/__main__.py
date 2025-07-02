import sqlite3

from runner.pos import app

connection = sqlite3.connect("../tests/testing_pos.db")

cursor = connection.cursor()

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

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS units (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS receipt_info (
        id TEXT PRIMARY KEY,
        status TEXT,
        total FLOAT
    )
"""
)

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
connection.commit()
connection.close()

if __name__ == "__main__":
    app()
