from typing import Union
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from propelauth_fastapi import init_auth
import os
from server.routers import data
from propelauth_py.user import User

from server.db import schemas
from server.db.dependencies import get_db

PROPELAUTH_API_KEY = os.environ.get("PROPELAUTH_API_KEY")
PROPELAUTH_AUTH_URL="https://58121323173.propelauthtest.com"
auth = init_auth(PROPELAUTH_AUTH_URL, PROPELAUTH_API_KEY)


app= FastAPI()
app.include_router(data.router)
