from pymongo.collection import Collection
from db import *
from credential import *
from fastapi import HTTPException, Request,Body
import models

#get all collection of library database
def get_collection(collection_name:str) -> Collection:
    return db[collection_name]

#create a user and add into user collection
def create_user(data):
    user_collection = db.get_collection("user")
    data = dict(data)
    data["password"] = get_password_hash(data["password"])
    response = user_collection.insert_one(data)
    return str(response.inserted_id)

#create a user and add into admin collection
def create_admin(data):
    admin_collection = db.get_collection("admin")
    data = dict(data)
    data["password"] = get_password_hash(data["password"])
    response = admin_collection.insert_one(data)
    return str(response.inserted_id)

# #add data into books collection
def add_books(data,current_admin:dict = Depends(get_current_admin)):
    admin_id = get_curr_admin(current_admin)
    book_collection = db.get_collection("books")
    data = dict(data)
    data.update({"admin_id":admin_id["admin_id"]})
    response = book_collection.insert_one(data)
    return str(response.inserted_id)

#view all books from books collection
def view_books():
    book_collection = db.get_collection("books")
    response = book_collection.find()
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

#get one book from books collection
def get_one_book(book_id:str):
    book_collection = db.get_collection("books")
    response = book_collection.find_one({"book_id":book_id})
    response["_id"] = str(response["_id"])
    return response

#get books by admin wise
def get_admin_books(current_admin:dict = Depends(get_current_admin)):
    admin_id = get_curr_admin(current_admin)
    book_collection = db.get_collection("books")
    response = book_collection.find({"admin_id":admin_id["admin_id"]})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])
        data.append(i)
    return data

#delete book add by admin
def delete_book(book_id,current_admin:dict = Depends(get_current_admin)):
    book_collection = db.get_collection("books")
    admin_id = get_curr_admin(current_admin)
    response = book_collection.delete_one({"book_id":book_id,"admin_id":admin_id["admin_id"]})
    return response.deleted_count

#issue book
def issue_book(data,book_id:str,current_user:dict = Depends(get_current_user)):
    book_collection = db.get_collection("books")
    user_collection = db.get_collection("user")
    issue_collection = db.get_collection("issueBook")
    user_id = get_curr_user(current_user)
    user_res = user_collection.find_one({"user_id":user_id["user_id"]})
    user_res["_id"] = str(user_res["_id"])
    if user_res:
        book_res = book_collection.find_one({"book_id":book_id})
        book_res["_id"] = str(book_res["_id"])
        if book_res:
            data = dict(data)
            data.update({"issue_id":data["issue_id"],"user_id":user_id["user_id"],"book_id":book_id,"card_id":user_res["card_id"],"username":user_res["username"],"issue_date":models.current_date,"due_date":models.future_date,"return_date":""})
            issue_id = issue_collection.find_one({"issue_id":data["issue_id"]})
            if not issue_id:
                response = issue_collection.insert_one(data)
                iss_res = issue_collection.find_one({"book_id":book_id})
                iss_res["_id"] = str(iss_res["_id"])
                upt_sts = book_collection.update_one({"book_id":book_id},{"$set":{"status":"Issued"}})
                return iss_res
            else:
                raise HTTPException(400,"issue id already found")
        else:
            raise HTTPException(404,"Book ID not found")
    else:
        raise HTTPException(404,"User not found")
            
#return issued book
def return_book(book_id:str,current_user:dict = Depends(get_current_user)):
    book_collection = db.get_collection("books")
    issue_collection = db.get_collection("issueBook")
    user_id = get_curr_user(current_user)
    book_res = book_collection.find_one({"book_id":book_id})
    if book_res:
        issue_res = issue_collection.find_one({"book_id":book_id})
        if not issue_res:
            del_issue_book = issue_collection.update_one({"book_id":book_id},{"$set":{"return_date":models.current_date}})
            upt_book = book_collection.update_one({"book_id":book_id},{"$set":{"status":"Available"}})
            return "Book Returned"
        else:
            raise HTTPException(404,"Book Id already found")
    else:
        raise HTTPException(404,"Book ID not found")
        