from fastapi import APIRouter, Depends, HTTPException
from .auth_users import auth_user
from db.client import db_client

from db.models.product import Product        # <--- USAR EL MODELO REAL
from db.schemas.products import product_schema, products_schema

from bson import ObjectId

router = APIRouter(prefix="/productsdb", tags=["productsdb"])


# ================================
# GET ALL
# ================================
@router.get("/", response_model=list[Product])
async def get_products():
    return products_schema(db_client.test.products.find())


# ================================
# GET BY QUERY ?id=
# ================================
@router.get("", response_model=Product)
async def get_product(id: str):
    return search_product_id(id)


# ================================
# GET BY ID /{id}
# ================================
@router.get("/{id}", response_model=Product)
async def get_product_path(id: str):
    return search_product_id(id)


# ================================
# POST – ADD PRODUCT
# ================================
@router.post("/", status_code=201, response_model=Product)
async def add_product(product: Product, user=Depends(auth_user)):

    product_dict = product.model_dump()
    del product_dict["id"]   # Mongo lo genera

    inserted_id = db_client.test.products.insert_one(product_dict).inserted_id
    product_dict["id"] = str(inserted_id)

    return Product(**product_dict)


# ================================
# PUT – MODIFY PRODUCT
# ================================
@router.put("/{id}", response_model=Product)
async def modify_product(id: str, product: Product):

    product_dict = product.model_dump()
    del product_dict["id"]

    try:
        db_client.test.products.find_one_and_replace(
            {"_id": ObjectId(id)},
            product_dict
        )
        return search_product_id(id)

    except:
        raise HTTPException(status_code=404, detail="Product not found")


# ================================
# DELETE – REMOVE PRODUCT
# ================================
@router.delete("/{id}", response_model=Product)
async def delete_product(id: str):

    found = db_client.test.products.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Product not found")

    return Product(**product_schema(found))


# ================================
# HELPERS
# ================================
def search_product_id(id: str):
    try:
        product = product_schema(
            db_client.test.products.find_one({"_id": ObjectId(id)})
        )
        return Product(**product)
    except:
        raise HTTPException(status_code=404, detail="Product not found")
