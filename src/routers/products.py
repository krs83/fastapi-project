from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{user_id}/orders", tags=["orders"])

cart_db = {}
product_id_counter = 1


# Show all products in the cart handler
@router.get("", status_code=200)
async def get_cart() -> list[Any] | dict[str, str]:
    if len(cart_db) > 0:
        return list(cart_db.values())
    else:
        return {"message": "your cart is still empty"}


# Add the product to the cart handler
@router.post("", status_code=201)
async def add_product(category: str, title: str, quantity: int):
    global product_id_counter

    for existing_product in cart_db.values():
        if (existing_product["category"] == category
                and existing_product["title"] == title):
            existing_product["quantity"] += quantity

            return cart_db

    product_id = product_id_counter
    product_id_counter += 1

    added_product = {
        "id": product_id,
        "category": category,
        "title": title,
        "quantity": quantity,
    }

    cart_db[product_id] = added_product

    return added_product


# Delete the product from the cart handler
@router.delete("/{product_id}", status_code=200)
async def delete_product_from_cart(product_id: int) -> dict[str, str]:
    await check_product_in_cart(product_id)

    del cart_db[product_id]
    return {"message": f"the product: id {product_id} is deleted from the cart"}


# Delete all products from the cart handler
@router.delete("", status_code=200)
async def delete_all_products_from_cart() -> dict[str, str]:
    cart_db.clear()

    return {"message": "your cart is empty now"}


async def check_product_in_cart(product_id: int) -> None:
    if product_id not in cart_db:
        raise HTTPException(status_code=404, detail="Product not found")
