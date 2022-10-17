from provider import CustomProvider
from open_feature import open_feature

from fastapi import FastAPI

app = FastAPI()

open_feature.provider = CustomProvider()
client = open_feature.client("fast-api-demo", "1.0.0")


@app.get("/")
async def root():
    greeting = client.get_string_value("greeting", "Hello World!")
    return {"message": greeting}


@app.post("/provider/storage")
async def provider_flag(storage: dict):
    open_feature.provider.storage = storage
    return {"message": "Provider storage updated"}
