from .users.routers import router as users_router
from .publications.routers import publications_router, comments_router
from .auth import router as auth_router

from fastapi import APIRouter


router = APIRouter(prefix='/api/v1')

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(publications_router)
router.include_router(comments_router)
