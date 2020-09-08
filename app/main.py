from typing import Optional
from fastapi import FastAPI
from sqlalchemy.sql import text
from query import get_stats

app = FastAPI()

@app.get("/")
def read_root():
    return {"REST API": "up and running"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/stats/{item_id}")
def read_stats(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

dummy_data = [i for i in range(100)]

# @app.get("/my/page/items/")
# async def read_item(page: int = 0, limit: int = 0, skip: int = 1):
#     return dummy_data[page*10: page*10 + limit: skip]

# metrics = ['NumberofServices', 'NumberofMedicareBeneficiaries']
# filters = {'CountryCodeoftheProvider': 'AR'}
# df = get_stats(metrics, filters)
# result = df.min()
# print(result.to_json())