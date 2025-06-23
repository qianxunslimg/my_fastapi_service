from fastapi import FastAPI, HTTPException, Query
from loguru import logger
import os
from api.router import api_router


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger.add(
    os.path.join(log_dir, "app.log"),
    rotation="50 MB",
    retention="30 days",
    compression="zip"
)

app = FastAPI(title = "yzc test service" )
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"msg": "Hello, API 正常运行"}

