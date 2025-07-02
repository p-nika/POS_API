from core.units import Unit, UnitsIterator
from infrastructure.units_repository import BasicUnitsIterator


def test_units_iterator() -> None:
    unit: Unit = Unit("Sample")
    iterator: UnitsIterator = BasicUnitsIterator([unit])
    assert iterator.has_next()
    assert iterator.next_unit() == unit
