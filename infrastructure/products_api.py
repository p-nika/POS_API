from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.products import ProductIterator, StoreItem
from core.products_errors import BarcodeExistsError, ItemNotExistsError
from core.units_error import UnitNotExistsError
from infrastructure.dependables import ItemsRepositoryDependable
from infrastructure.products import Product

products_api = APIRouter(tags=["products"])


class ProductModel(BaseModel):
    id: UUID
    unit_id: UUID
    name: str
    barcode: str
    price: float


class CreateProductResponse(BaseModel):
    product: ProductModel


class CreateProductRequest(BaseModel):
    unit_id: UUID
    name: str
    barcode: str
    price: float


class ProductListResponse(BaseModel):
    products: List[ProductModel]


class UpdatePriceRequest(BaseModel):
    price: float


@products_api.post("/products", status_code=201, response_model=CreateProductResponse)
def create_product(
    request: CreateProductRequest, products: ItemsRepositoryDependable
) -> Dict[Any, Any] | JSONResponse:
    item: StoreItem = Product(**request.model_dump())
    try:
        products.add_product(item)
        return {"product": item}
    except BarcodeExistsError:
        return JSONResponse(
            status_code=409,
            content={
                "message": f"item with barcode <{item.get_barcode()}> already exists."
            },
        )
    except UnitNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Unit with id <{item.get_unit_id()}> does not exist."},
        )


@products_api.get(
    "/products/{product_id}", status_code=200, response_model=ProductModel
)
def get_product(
    product_id: UUID, products: ItemsRepositoryDependable
) -> StoreItem | JSONResponse:
    try:
        return products.get_product(product_id)
    except ItemNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"item with id <{product_id}> doesn't exist."},
        )


@products_api.get("/products", status_code=200, response_model=ProductListResponse)
def get_all_products(products: ItemsRepositoryDependable) -> Dict[Any, Any]:
    iterator: ProductIterator = products.get_all_products()
    all_products: List[StoreItem] = []
    while iterator.has_next():
        all_products.append(iterator.next_item())
    return {"products": all_products}


@products_api.patch(
    "/products/{product_id}", status_code=200, response_model=Dict[Any, Any]
)
def update_price(
    product_id: UUID, request: UpdatePriceRequest, products: ItemsRepositoryDependable
) -> Dict[Any, Any] | JSONResponse:
    try:
        new_price: float = request.model_dump()["price"]
        products.update_price(product_id, new_price)
        return {}
    except ItemNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"item with id <{product_id}> doesn't exist."},
        )
