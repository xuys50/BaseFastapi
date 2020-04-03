from fastapi import  FastAPI
from routers import  users
from app.user import models
from setting import  engine,oauth2_scheme
from fastapi import  Depends

# main进入的时候创建所有的数据库 相当于初始化
models.Base.metadata.create_all(bind=engine)
# from app.Item import  models
# models.Base.metadata.creat_all(bind=engine)


app = FastAPI()

# 首页路径
@app.get("/")
def root():
    return {
        "hello":"helloworld",
        "desc":"http://127.0.0.1:8000/docs"
    }


app.include_router(
    users.router,
    prefix='/users',
    tags=['users'],
)
