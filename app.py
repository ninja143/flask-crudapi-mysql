import uuid
from flask import Flask, request
from db import items
app = Flask(__name__)

# Databse Connection 
"""
import connect_to_mysql
config = {"host": "127.0.0.1", "user": "root", "password": "db@12345", "database": "flask_crud"}
try:
    cnx=connect_to_mysql.connect(config, attempts=1)
    print("Datatabe Conected !!!")
except ConnectionError as e:
    print(f"Error: {e}")
"""


@app.route("/")
def home():
    '''Base Route: Welcome to Flask CRUD Rest API'''
    return "CRUD App"

@app.post("/item")
def add_item():
    '''Add Item Api'''
    req_data = request.get_json()
    if "name" not in req_data or "price" not in req_data or "is_available" not in req_data:
        return {"status": 400, "message" : 'Parameter missing !'}
    try:
        items[uuid.uuid4().hex] = req_data
        return {
            "status": 201,
            "message": "Item is added sucessfully." 
        }
    except: 
        return {
            "status": 500,
            "message": "Something went wrong, please try later" 
        }
    
@app.get("/item/<string:name>")
def get_item(name):
    '''Get Item Api'''
    if request.args.get('id') is None:
        return {
            "status": 200, 
            "data": items
        }
    try:
        for item in items:
            if name == item["name"]:
                return {
                    "status": 200, 
                    "data": item
                }

        return {
            "status": 200, 
            "message": 'Item not found.' 
        }
    except: 
        return {
            "status": 400, 
            "message": 'Bad request' 
        }
        
@app.get("/item")
def find_item():
    '''Get Item Api By Arguments'''
    item_id = request.args.get('id')
    if item_id is None:
        return {
            "status": 200, 
            "data": items
        }
    
    try:
        return {
            "status": 200,
            "data": items[item_id]
        }
    except KeyError:
        return {
            "status": 200, 
            "message": 'record not found' 
        }

@app.put("/item")
def update_item():
    '''Update Item Api'''
    item_id = request.args.get('id')
    if item_id in items.key():
        request_data = request.get_json()
        items[item_id]["name"] = request_data["name"]
        items[item_id]["price"] = request_data["price"]
        return {
            "status": 201,
            "message": "item updated successfully."
        }
    return {
        "status": 404,
        "message": 'not found'
    }

@app.delete("/item")
def delete_item():
    '''Update Item Api'''
    item_id = request.args.get('id')
    if item_id in items.keys():
        del items[item_id]
        return { "status": 200, "message": "item deleted successfully." }
    return {
        "status": 404,
        "message": 'record does not exist'
    }
