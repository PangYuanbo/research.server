from fastapi import FastAPI, APIRouter
from propelauth_fastapi import init_auth, User
auth = init_auth("admin", "5353c7e2a8f8cf5a03cf5e5d4e649215b308f612dbb4abeaa64cb257d056356703889b7e5db54398e89c08416b605860")
router = APIRouter()
@router.get("/auth")
