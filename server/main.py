import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi import Request
from fastapi.responses import Response
from propelauth_fastapi import init_auth, User as AuthUser
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from server.db.dependencies import get_db
from server.db.model import Users

load_dotenv()
AUTH_URL = os.getenv("AUTH_URL")
API_KEY = os.getenv("API_KEY")
PROXY_URL = os.getenv("PROXY_URL")
auth = init_auth(AUTH_URL, API_KEY)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(current_user: AuthUser = Depends(auth.require_user)):
    return {"message": f"Hello {current_user.user_id}"}


@app.get("/users/me")
async def read_users_me(current_user: AuthUser = Depends(auth.require_user), db: Session = Depends(get_db)):
    user_id = current_user.user_id
    db_user = db.query(Users).where(Users.user_id == user_id).first()
    if db_user is None:
        # create a new user
        db_user = Users(user_id=user_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
# 动态路径，可以捕获任何 '/...' 的请求
async def proxy_request(path: str, request: Request, current_user: AuthUser = Depends(auth.require_user)):
    # 目标URL，将请求转发到此URL
    target_url = f"{PROXY_URL}/{path}"
    # 创建异步客户端
    async with httpx.AsyncClient() as client:
        # 获取原始请求体
        body = await request.body()

        # 获取原始请求头部并去除一些不适合转发的头部
        headers = dict(request.headers)
        headers.pop("host", None)  # 不转发host头部，因为这会导致问题
        headers.pop("content-length", None)  # 让 httpx 自动计算

        # 发送请求到目标URL
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            # 转发查询参数并且拼接 current_user.user_id 作为查询参数
            params={**request.query_params, "user_id": current_user.user_id},
        )

        # 返回从目标URL获取的响应
        return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

# app.include_router(userdata.router)
# app.include_router(researchdate.router)
# app.include_router(application.router)
