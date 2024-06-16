from fastapi import FastAPI
from loguru import logger
import os
from db.model_orm import *
from db.model_schema import *
from db.db import init

app = FastAPI()
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger.add(
    os.path.join(log_dir, "app.log"),
    rotation="50 MB",  # 单个日志文件大小
    retention="30 days",  # 日志保留时间
    compression="zip"  # 日志文件压缩格式
)


@app.on_event("startup")
async def startup_event():
    await init()


@app.get("/")
async def root():
    first_db = await Item.create_with_id()
    first_db.name = f"name_{first_db.id}"
    first_db.description = f"description_{first_db.id}"

    await first_db.save()
    logger.info(f"fuck u")
    return {"Hello": "World"}


@app.get("/items", response_model=List[ItemData])
async def read_items():
    logger.info("Request to read items.")
    items = await Item.all()
    return items
