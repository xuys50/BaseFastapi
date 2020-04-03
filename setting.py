from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import  sessionmaker
import jwt
from jwt import PyJWTError
from passlib.context import  CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

"""====================Connect===================="""
# 创建数据库
sql_url = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# 数据库实例
engine = create_engine(
    sql_url,
    echo=False,
    connect_args = {
        "check_same_thread": False
    }
)
# check_same_thread这个是sqllite必须添加的，其他数据库不用

# 建立连接
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
# 创建连接实例
Base = declarative_base()


"""====================JWt===================="""

SALT_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 这个一定要和请求token的url一直  也就是access方法，同意改成Login把
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")



