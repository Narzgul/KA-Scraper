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
    products = []
    with open("products.txt") as products_file:
        for line in products_file:
            products.append(line.split(',')[1].strip())

    return products


@api.get("/products/{name}")
async def get_ads_by_name(name):
    return cursor.execute("SELECT * FROM products WHERE category == '" + name + "' ORDER BY CAST(product_id AS INTEGER)").fetchall()
