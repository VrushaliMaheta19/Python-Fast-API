from crud import *
from fastapi import FastAPI
import models, credential
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app = FastAPI()

token_url = "userLogin"
oauth2 = OAuth2PasswordBearer(tokenUrl=token_url)

@app.post("/createUser")
def createUser(data:models.User):
    id = create_user(data)
    return {"Inserted":True,"Inserted id":id}

@app.post("/createAdmin")
def createAdmin(data:models.Admin):
    id = create_admin(data)
    return {"Inserted":True,"Inserted id":id}

@app.post("/user/Login")
def userLogin(data:OAuth2PasswordRequestForm = Depends()):
    usr_data = user_login(data)
    return usr_data

@app.post("/admin/Login")
def adminLogin(data:OAuth2PasswordRequestForm = Depends()):
    usr_data = admin_login(data)
    return usr_data

@app.get("/user/currentUser")
def currentUser(curr_user:dict = Depends(get_current_user)):
    data = get_curr_user(curr_user)
    return data

@app.get("/admin/currentAdmin")
def currentAdmin(curr_user:dict = Depends(get_current_admin)):
    data = get_curr_admin(curr_user)
    return data

@app.post("/admin/addBooks")
def addBooks(data:models.Books,current_admin:dict = Depends(get_current_admin)):
    id = add_books(data,current_admin)
    return {"Inserted":True,"Inserted id":id}

@app.get("/viewBooks")
def viewBooks():
    data = view_books()
    return {"data":data}

@app.get("/viewOneBook/{book_id}")
def viewOneBook(book_id:str):
    data = get_one_book(book_id=book_id)
    return {"data":data}

@app.get("/admin/viewAdminBook/")
def viewAdminBooks(current_admin:dict = Depends(get_current_admin)):
    data = get_admin_books(current_admin)
    return {"data":data}

@app.delete("/admin/deleteBook/{book_id}")
def deleteBook(book_id:str,current_admin:dict = Depends(get_current_admin)):
    data = delete_book(book_id,current_admin)
    return {"Deleted item count":data}

@app.put("/user/issueBook/{book_id}",response_model=models.issueBook)
def issueBook(data:models.issueBookDB,book_id:str,current_user:dict = Depends(get_current_user)):
    data = issue_book(data,book_id,current_user)
    return data

@app.put("/user/returnBook/{book_id}")
def returnBook(book_id:str,current_user:dict = Depends(get_current_user)):
    data = return_book(book_id,current_user)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)