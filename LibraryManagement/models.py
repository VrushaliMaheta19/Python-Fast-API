from pydantic import BaseModel, EmailStr, Field
from datetime import datetime,timedelta

date = datetime.now().date()
current_date = date.strftime("%d/%m/%Y")

f_date = date + timedelta(days=15)
future_date = f_date.strftime("%d/%m/%Y")

class User(BaseModel):
    user_id:str
    username:str
    password:str
    email:EmailStr
    mobile_no:str
    card_id:str

class Admin(BaseModel):
    admin_id:int
    username:str
    password:str
    email:EmailStr
    mobile_no:str

class Books(BaseModel):
    book_id:str
    admin_id:int
    name:str
    author:str
    status:str = Field(default="Available")

class issueBook(BaseModel):
    issue_id:int
    user_id:str
    book_id:str
    card_id:str
    username:str
    issue_date:str = Field(default=current_date)
    due_date:str = Field(default=future_date)
    return_date:str = None
    
class issueBookDB(BaseModel):
    issue_id:int
