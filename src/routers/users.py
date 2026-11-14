

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/users", tags=["users"])

users_db = {}
user_id_counter = 1

@router.get("", status_code=200)
async def get_users(page: int = Query(1, ge=1, description="Page number"),
                    limit: int = Query(10, ge=1, le=100, description="Page quantity"),):
    start = (page - 1) * limit
    end = start + limit
    users = list(users_db.values())
    return {
        "page": page,
        "limit": limit,
        "total": len(users),
        "items": users[start:end]
    }

@router.get("/{user_id}", status_code=200)
async def get_user(user_id: int):
    await check_user(user_id)

    return users_db[user_id]

@router.post("", status_code=201)
async def create_user(name: str, email: str):
    global user_id_counter

    for existing_user in users_db.values():
        if existing_user["email"] == email:
            raise HTTPException(status_code=400, detail="Email already registered")

    user_id = user_id_counter
    user_id_counter += 1

    new_user = {
        "id": user_id,
        "name": name,
        "email": email,
        "is_active": True,
    }
    users_db[user_id] = new_user

    return new_user

@router.put("/{user_id}")
async def update_user(user_id: int, name: str, email: str):
    await check_user(user_id)

    current_user = users_db[user_id]

    for existing_user in users_db.values():
        if existing_user["email"] == email and existing_user["id"] != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")

        current_user["name"] = name
        current_user["email"] = email

    return current_user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    await check_user(user_id)

    del users_db[user_id]
    return {"message":f"the user:{user_id} is deleted"}


async def check_user(user_id: int) -> None:
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")