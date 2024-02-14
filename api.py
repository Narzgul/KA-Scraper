import sqlite3
from fastapi import FastAPI

connection = sqlite3.connect("scraper_objects_data")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

for element in cursor.execute("Select * from products"):
    print(element)

api = FastAPI()


# Start with: uvicorn api:api --reload
@api.get("/products")
async def get_products():
    return cursor.execute("SELECT * FROM products").fetchall()
