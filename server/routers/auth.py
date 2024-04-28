from fastapi import FastAPI, APIRouter
from propelauth_fastapi import init_auth, User
router = APIRouter()
@router.get("/auth")
