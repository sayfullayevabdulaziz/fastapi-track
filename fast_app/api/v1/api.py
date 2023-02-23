from fastapi import APIRouter

from fast_app.api.v1.endpoints import user, login, role, track, blog, comment

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(role.router, prefix="/role", tags=["role"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(track.router, prefix="/track", tags=["track"])
api_router.include_router(blog.router, prefix="/blog", tags=["blog"])
api_router.include_router(comment.router, prefix="/comment", tags=["comment"])