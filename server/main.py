from fastapi import FastAPI, Depends
from server.routers import userdata, researchdate, application
from propelauth_fastapi import init_auth,User
import os
AUTH_URL = os.getenv("AUTH_URL")
API_KEY = os.getenv("API_KEY")
auth = init_auth(AUTH_URL, API_KEY)
app= FastAPI()
@app.get("/")
async def root(current_user: User = Depends(auth.require_user)):
    return {"message": f"Hello {current_user.user_id}"}
app.include_router(userdata.router)
app.include_router(researchdate.router)
app.include_router(application.router)