import sqlite3
from fastapi import FastAPI

connection = sqlite3.connect("scraper_objects_data")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

api = FastAPI()


# Start with: uvicorn api:api --reload
@api.get("/")
async def root():
    return "Hello World"


@api.get("/products")
async def get_products():
    return cursor.execute("SELECT * FROM products ORDER BY CAST(product_id AS INTEGER)").fetchall()
