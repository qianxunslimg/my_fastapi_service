from fastapi import FastAPI
from loguru import logger
import os

app = FastAPI()

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger.add(
    os.path.join(log_dir, "app.log"), 
    rotation="50 MB",  # 单个日志文件大小
    retention="30 days",  # 日志保留时间
    compression="zip"  # 日志文件压缩格式
)

@app.get("/")
def root():
    logger.info(f"fuck u")
    return {"Hello": "World"}
