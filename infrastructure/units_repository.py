from sqlite3 import Cursor
from typing import List
from uuid import UUID

from core.units import Unit, UnitsIterator
from core.units_error import UnitExistsError, UnitNotExistsError
from core.units_repository import UnitsRepository
from infrastructure.database_handler import ConnectionHandler


class BasicUnitsIterator(UnitsIterator):
    units: List[Unit]
    current_index: int

    def __init__(self, all_units: List[Unit]):
        self.units = all_units
        self.current_index = 0

    def has_next(self) -> bool:
        return len(self.units) > self.current_index

    def next_unit(self) -> Unit:
        result: Unit = self.units[self.current_index]
        self.current_index += 1
        return result


class UnitsInBase(UnitsRepository):
    _handler: ConnectionHandler

    def __init__(self, connection_handler: ConnectionHandler):
        self._handler = connection_handler
        self._handler.create_connection()

    def assert_unique_name(self, unit: Unit) -> bool:
        cursor: Cursor = self._handler.get_cursor()
        check_query: str = f"SELECT * FROM units WHERE name = '{unit.get_name()}'"
        cursor.execute(check_query)
        result: List[str] = cursor.fetchone()
        if result is not None:
            raise UnitExistsError(unit)
        else:
            return False

    def assert_unit_exists(self, unit_id: UUID) -> bool:
        cursor: Cursor = self._handler.get_cursor()
        check_query: str = f"SELECT * FROM units WHERE id = '{unit_id}'"
        cursor.execute(check_query)
        result: List[str] = cursor.fetchone()
        if result is None:
            raise UnitNotExistsError(unit_id)
        return True

    def add_unit(self, unit: Unit) -> None:
        self.assert_unique_name(unit)
        cursor: Cursor = self._handler.get_cursor()
        insert_unit_query: str = (
            f"INSERT INTO units (id, name) "
            f"VALUES ('{unit.get_id()}', '{unit.get_name()}')"
        )
        cursor.execute(insert_unit_query)
        self._handler.commit_connection()

    def get_unit(self, unit_id: UUID) -> Unit:
        self.assert_unit_exists(unit_id)
        cursor: Cursor = self._handler.get_cursor()
        get_unit_query: str = f"SELECT * FROM units WHERE id = '{unit_id}'"
        cursor.execute(get_unit_query)
        result: List[str] = cursor.fetchone()
        return self.create_unit(result)

    def get_all_units(self) -> UnitsIterator:
        cursor: Cursor = self._handler.get_cursor()
        get_unit_query: str = "SELECT * FROM units"
        cursor.execute(get_unit_query)
        all_units: List[Unit] = []
        result: List[List[str]] = cursor.fetchall()
        for row in result:
            all_units.append(self.create_unit(row))
        return BasicUnitsIterator(all_units)

    @staticmethod
    def create_unit(row: List[str]) -> Unit:
        return Unit(row[1], UUID(row[0]))
