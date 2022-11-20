from .users.routers import router as users_router
from .publications.routers import comments_router, publications_router

from fastapi import APIRouter


router = APIRouter(prefix='/api/v1')

router.include_router(users_router)
router.include_router(publications_router)
router.include_router(comments_router)
