from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.units import Unit, UnitsIterator
from core.units_error import UnitExistsError, UnitNotExistsError
from infrastructure.dependables import UnitsRepositoryDependable

units_api = APIRouter(tags=["units"])


class UnitRequest(BaseModel):
    name: str


class UnitModel(BaseModel):
    id: UUID
    name: str


class UnitResponse(BaseModel):
    unit: UnitModel


class UnitListResponse(BaseModel):
    units: List[UnitModel]


@units_api.post("/units", status_code=201, response_model=UnitResponse)
def create_unit(
    request: UnitRequest, units: UnitsRepositoryDependable
) -> Dict[Any, Any] | JSONResponse:
    new_unit: Unit = Unit(**request.model_dump())
    try:
        units.add_unit(new_unit)
        return {"unit": new_unit}
    except UnitExistsError:
        return JSONResponse(
            status_code=409,
            content={
                "message": f"Unit with name <{new_unit.get_name()}> already exists."
            },
        )


@units_api.get("/units/{unit_id}", status_code=200, response_model=UnitResponse)
def get_unit(
    unit_id: UUID, units: UnitsRepositoryDependable
) -> Dict[Any, Any] | JSONResponse:
    try:
        return {"unit": units.get_unit(unit_id)}
    except UnitNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Unit with id <{unit_id}> does not exist."},
        )


@units_api.get("/units", status_code=200, response_model=UnitListResponse)
def get_all_units(units: UnitsRepositoryDependable) -> Dict[Any, Any]:
    units_iterator: UnitsIterator = units.get_all_units()
    all_units: List[Unit] = []
    while units_iterator.has_next():
        all_units.append(units_iterator.next_unit())
    return {"units": all_units}
