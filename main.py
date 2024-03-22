from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["https://localhost:3000"],
    allow_methods = ['*'],
    allow_headers = ['*']
)

redis = get_redis_connection(
    host = 'redis-15846.c264.ap-south-1-1.ec2.cloud.redislabs.com',
    port = '15846',
    password = "7dTLW3g4A226qEq5CfohqXWadkW4ZTZA",
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
    return Product.all_pks()