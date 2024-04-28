
from fastapi import FastAPI
from propelauth_fastapi import init_auth
import os
from server.routers import userdata, researchdate, application

app= FastAPI()
app.include_router(userdata.router)
app.include_router(researchdate.router)
app.include_router(application.router)