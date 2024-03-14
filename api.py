import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel


class NewProduct(BaseModel):
    name: str
    link: str


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
    return cursor.execute(
        "SELECT * FROM products WHERE category == '" + name + "' ORDER BY CAST(product_id AS INTEGER)").fetchall()


@api.post("/new_product")
async def new_product(new_product: NewProduct):
    with open("products.txt", "a") as products_file:
        products_file.write(new_product.link + ',' + new_product.name + '\n')


@api.delete("/products/{name}")
async def delete_product(name):
    with open("products.txt", "r+") as products_file:
        lines = products_file.readlines()
        products_file.seek(0)
        # Write every line except the one that contains name
        for line in lines:
            if line.split(',')[1].strip() != name:
                products_file.write(line)
        products_file.truncate()  # End file at current pointer location

    # Remove all relevant products from the database
    cursor.execute("DELETE FROM products WHERE category == '" + name + "'")
    connection.commit()
