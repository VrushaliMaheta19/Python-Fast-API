There 5 API files

credential.py - contains authorization of user and admin
crud.py - contains CRUD operation(like, view,issue,add books, delete books, etc. operations)
db.py - contains connectivity URL with the MongoDB database
models.py - contains schema structure to store in to MongoDB collection
main.py - maintains API request(get, post, delete, etc) 

In the backend use MongoDB database
Database name - library
collection name - books
                  user
                  admin
                  issueBook
