from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
import os

load_dotenv()

redis_api_key = os.environ.get('REDIS_KEY')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://localhost:3000"],
    allow_methods = ['*'],
    allow_headers = ['*']
)

redis = get_redis_connection(
    host = redis_host,
    port = redis_port,
    password = redis_api_key,
    decode_responses = True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    class Meta:
        database = redis

@app.post("/product")
def create(product: Product):
    return product.save()

@app.get("/product/{pk}")
def get_product(pk: str):
    return Product.get(pk)

@app.get("/products")
def get_all_products():
    #return Product.all_pks()
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity

    }

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
