
from fastapi import FastAPI
from propelauth_fastapi import init_auth
import os
from server.routers import data


PROPELAUTH_API_KEY = os.environ.get("PROPELAUTH_API_KEY")
PROPELAUTH_AUTH_URL="https://58121323173.propelauthtest.com"
auth = init_auth(PROPELAUTH_AUTH_URL, PROPELAUTH_API_KEY)


app= FastAPI()
app.include_router(data.router)
