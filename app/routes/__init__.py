from fastapi.routing import APIRouter

from .root import root

api_router = APIRouter()

api_router.include_router(root)
