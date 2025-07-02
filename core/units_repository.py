from typing import Protocol
from uuid import UUID

from core.units import Unit, UnitsIterator


class UnitsRepository(Protocol):
    def add_unit(self, unit: Unit) -> None:
        pass

    def get_unit(self, unit_id: UUID) -> Unit:
        pass

    def get_all_units(self) -> UnitsIterator:
        pass

    def assert_unit_exists(self, unit_id: UUID) -> bool:
        pass
