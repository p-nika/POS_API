import uuid
from typing import Protocol
from uuid import UUID


class Unit:
    id: UUID
    name: str

    def __init__(self, name: str, unit_id: UUID = uuid.uuid4()):
        self.id = unit_id
        self.name = name

    def get_id(self) -> UUID:
        return self.id

    def get_name(self) -> str:
        return self.name


class UnitsIterator(Protocol):
    def has_next(self) -> bool:
        pass

    def next_unit(self) -> Unit:
        pass
