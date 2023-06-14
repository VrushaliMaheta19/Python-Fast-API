from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import *
import jwt
from fastapi import HTTPException, Depends

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#define token urls
token_url = "user/Login"
oauth2 = OAuth2PasswordBearer(tokenUrl=token_url,scheme_name="user_oauth2_scheme")

token_url1 = "admin/Login"
oauth1 = OAuth2PasswordBearer(tokenUrl=token_url1,scheme_name="admin_oauth2_scheme")

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

#password verification
def verify_password(plain_passord:str,hash_passsword:str):
    return pwd_context.verify(plain_passord,hash_passsword)

#get password hashing
def get_password_hash(password:str):
    return pwd_context.hash(password)

#authenticate user
def authenticate_user(username,password):
    user_collection = db.get_collection("user")
    user = user_collection.find_one({"username":username})
    if not user:
        return False
    if not verify_password(password,user["password"]):
        return False
    return user

#authenticate admin
def authenticate_admin(username,password):
    admin_collection = db.get_collection("admin")
    admin = admin_collection.find_one({"username":username})
    if not admin:
        return False
    if not verify_password(password,admin["password"]):
        return False
    return admin

#create access token
def create_access_token(data:dict,expire_data:timedelta | None = None):
    to_encode = data.copy()
    if expire_data:
        expire = datetime.utcnow() + expire_data
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"expire":str(expire)})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt 

#get current user
def get_current_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("user")
        user_collection = db.get_collection("user")
        user = user_collection.find_one({"username":username})
        user["_id"] = str(user["_id"])
        if not user:
            raise HTTPException(401,"Invalid Credentials")
        return user["user_id"]
    except:
        raise HTTPException(401,"Invalid Token")

#get current admin
def get_current_admin(token:str = Depends(oauth1)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("user")
        admin_collection = db.get_collection("admin")
        admin = admin_collection.find_one({"username":username})
        admin["_id"] = str(admin["_id"])
        if not admin:
            raise HTTPException(401,"Invalid Credentials")
        return admin["admin_id"]
    except:
        raise HTTPException(401,"Invalid Token")
 
#logged user   
def user_login(data:OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(data.username,data.password)
    if not user:
        raise HTTPException(401,"Invalid Username or Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"user":user["username"]},expire_data=access_token_expires)
    return {"access_token":access_token,"token_type":"Bearer"}

#logged admin
def admin_login(data:OAuth2PasswordRequestForm = Depends()):
    user = authenticate_admin(data.username,data.password)
    if not user:
        raise HTTPException(401,"Invalid Username or Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"user":user["username"]},expire_data=access_token_expires)
    return {"access_token":access_token,"token_type":"Bearer"}

#get current user id
def get_curr_user(current_user:dict = Depends(get_current_user)):
    return {"user_id":current_user}

#get current admin id
def get_curr_admin(current_admin:dict = Depends(get_current_admin)):
    return {"admin_id":current_admin}