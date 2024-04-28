
from fastapi import FastAPI
from propelauth_fastapi import init_auth
import os
from server.routers import data



app= FastAPI()
app.include_router(data.router)
