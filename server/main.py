from typing import Union
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from propelauth_fastapi import init_auth
import os

from propelauth_py.user import User

from server.db import schemas
from server.db.dependencies import get_db

PROPELAUTH_API_KEY = os.environ.get("PROPELAUTH_API_KEY")
PROPELAUTH_AUTH_URL="https://58121323173.propelauthtest.com"
auth = init_auth(PROPELAUTH_AUTH_URL, PROPELAUTH_API_KEY)


app= FastAPI()

@app.get("/api/whoami")
async def root(current_user: User = Depends(auth.require_user)):
    return {"user_id": f"{current_user.user_id}"}
