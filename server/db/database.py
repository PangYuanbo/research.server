import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
load_dotenv()

# 定义数据库连接字符串
DATABASE_URL = os.getenv("DB")

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# SessionLocal 是一个会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 类将用于后续的所有模型类
Base = declarative_base()
