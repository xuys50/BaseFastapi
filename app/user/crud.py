from sqlalchemy.orm import  Session
from app.user import  models
from pydantic import  BaseModel
from setting import  pwd_context,SALT_KEY,ALGO,oauth2_scheme
from datetime import datetime, timedelta
import jwt

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class TokenDesc(BaseModel):
    access_token: str
    token_type: str


# 对密码加密
def encryption_passwd(passwd: str):
    # return passwd + "notreallyhashed"
    return pwd_context.hash(passwd)

# 对密码进行校验 ,
# 1.对输入的密码进行加密
# 2. 获取对应的用户的密码
# 3. 校验密码

# 返回用户 存在user  不存在None
def verify_passwd(db:Session,passwd: str,email: str):
    user = get_user_by_email(db,email=email)
    if user:
        if not pwd_context.verify(passwd,user.hashed_password):
            return None
        # if user.hashed_password != passwd:
        #     return None
        else:
            return user
    else:
        return None

# 创建token
def create_access_token(*,data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=SALT_KEY,
        algorithm=ALGO)
    return encoded_jwt

# 对token进行解密，获取关键信息
def decryption_token(token: str,db:Session):
    data = jwt.decode(token,key=SALT_KEY,algorithms=ALGO)
    username = data.get('sub')
    user = db.query(models.User).filter(models.User.email == username).first()
    return user




# READ
def get_user(db:Session,user_id: int ):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id)



def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()



# Create
def create_user(db: Session, user: UserCreate):
    fake_hashed_password = encryption_passwd(user.password)
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    return db_user




