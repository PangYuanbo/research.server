from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from server.routers import userdata, researchdate, application
from propelauth_fastapi import init_auth,User
import os
load_dotenv()
AUTH_URL = os.getenv("AUTH_URL")
API_KEY = os.getenv("API_KEY")
auth = init_auth(AUTH_URL, API_KEY)
app= FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(current_user: User = Depends(auth.require_user)):
    return {"message": f"Hello {current_user.user_id}"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(auth.require_user)):
    return current_user

app.include_router(userdata.router)
app.include_router(researchdate.router)
app.include_router(application.router)