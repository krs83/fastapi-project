from src.routers.users import router as users_router
from src.routers.health import router as health_router
from src.routers.products import router as orders_router

__all__ = ["users_router", "health_router", "orders_router"]