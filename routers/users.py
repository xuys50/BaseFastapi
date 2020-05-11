from fastapi import APIRouter
from app.user import crud
from fastapi import  Depends, HTTPException,status
from sqlalchemy.orm import  Session
from setting import  SessionLocal,ACCESS_TOKEN_EXPIRE_MINUTES,oauth2_scheme
from fastapi.security import  OAuth2PasswordRequestForm

from datetime import  datetime,timedelta


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

router = APIRouter()


# 用户jwt版创建流程
# 注册:
# 1.输入用户信息
# 2. 判断用户是否存在，存在则返回404 不存在则继续
# 3. 提取用户密码，hash加密之后，存入数据库
# 第一次登录:
# 1. 获取用户信息，输入信息以UserCreate为模板输入
# 2. 根据email信息查看是否存在该用户，存在则继续，不存在则报错
# 3. 获取密码，对密码进行hash加密 ,与数据库中的密码对比，匹配成功则继续，错误则报错
# 4. 根据用户的账号和密码生成对应token
# 第二次之后登录
# 1. 用户拿着token去校验，首先需要对token进行解密，机密之后暴露用户信息


# 登录流程
@router.post("/login",response_model=crud.TokenDesc)
async def login_for_access_token(db: Session=Depends(get_db),form_data: OAuth2PasswordRequestForm=Depends()):
    user = crud.verify_passwd(db,form_data.password,form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 创建用户
@router.post("/", response_model=crud.User)
def create_user(user: crud.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# 获取当前用户信息
@router.get("/me",response_model=crud.User)
def read_item(token: str = Depends(oauth2_scheme),db: Session=Depends(get_db)):
    user = crud.decryption_token(token,db)
    return user

# 根据用户ID获取信息
@router.get("/{user_id}", response_model=crud.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

