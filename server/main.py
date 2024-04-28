import json
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi import Request
from fastapi.responses import Response
from propelauth_fastapi import init_auth, User as AuthUser
from starlette.middleware.cors import CORSMiddleware

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


# @app.get("/")
# async def root(current_user: AuthUser = Depends(auth.require_user)):
#     return {"message": f"Hello {current_user.user_id}"}


# @app.get("/users/me")
# async def read_users_me(current_user: AuthUser = Depends(auth.require_user), db: Session = Depends(get_db)):
#     user_id = current_user.user_id
#     db_user = db.query(Users).where(Users.user_id == user_id).first()
#     if db_user is None:
#         # create a new user
#         db_user = Users(user_id=user_id)
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#     return db_user


@app.api_route("/proxy/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
async def proxy_request(path: str, request: Request, current_user: AuthUser = Depends(auth.require_user)):
    target_url = f"{PROXY_URL}/{path}"

    async with httpx.AsyncClient() as client:
        # 尝试获取请求体，可能为空
        body = await request.body()

        # 准备请求头
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)  # httpx 自动计算内容长度

        # 检查内容类型是否为 JSON 并处理
        content_type = headers.get("content-type", "")
        if "application/json" in content_type:
            try:
                # 解码原始请求体并转换为 JSON 对象
                data = json.loads(body.decode())
                # 添加 current_user.user_id
                data["user_id"] = current_user.user_id
                # 重新编码修改后的 JSON 对象为请求体
                body = json.dumps(data).encode()
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON body")

        try:
            # 发送修改后的请求到目标URL
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params={**request.query_params, "user_id": current_user.user_id},
            )
            # 返回从目标URL获取的响应
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting {target_url}. {str(exc)}")


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
async def proxy_request(path: str, request: Request):
    target_url = f"{PROXY_URL}/{path}"

    async with httpx.AsyncClient() as client:
        # 尝试获取请求体，可能为空
        body = await request.body()

        # 准备请求头
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)  # httpx 自动计算内容长度

        # 检查内容类型是否为 JSON 并处理
        content_type = headers.get("content-type", "")
        if "application/json" in content_type:
            try:
                # 解码原始请求体并转换为 JSON 对象
                data = json.loads(body.decode())
                # 重新编码修改后的 JSON 对象为请求体
                body = json.dumps(data).encode()
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON body")

        try:
            # 发送修改后的请求到目标URL
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params,
            )
            # 返回从目标URL获取的响应
            return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting {target_url}. {str(exc)}")

# app.include_router(userdata.router)
# app.include_router(researchdate.router)
# app.include_router(application.router)
