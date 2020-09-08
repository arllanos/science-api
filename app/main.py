from typing import Optional, List
from fastapi import FastAPI, Query, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.sql import text
from pydantic import BaseModel
from query import get_stats
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"REST API": "up and running"}

def filters_dict(filters: List[str] = Query(...)):
    return list(map(json.loads, filters))

@app.get("/stats/metric/{metric_id}")
async def read_single_metric_stats(metric_id: str, filter: list = Depends(filters_dict)):
    d_filters = {k: v for d in filter for k, v in d.items()}
    stats = get_stats(metric_id, d_filters)
    return stats
