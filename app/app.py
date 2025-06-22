from fastapi import FastAPI, HTTPException, Query
from loguru import logger
import pandas as pd
import requests
from io import BytesIO
import os

app = FastAPI()

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger.add(
    os.path.join(log_dir, "app.log"),
    rotation="50 MB",
    retention="30 days",
    compression="zip"
)

def download_excel(url: str) -> BytesIO:
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"下载失败，状态码：{response.status_code}")

def is_invalid_name(name):
    if pd.isna(name):
        return True
    name = str(name).strip()
    if (("班" in name and len(name) <= 3) or (name.upper() == "DSE")):
        return True
    return False

def analyze_excel(url: str):
    try:
        excel_file = download_excel(url)
        df = pd.read_excel(excel_file)

        df = df[~df['姓名/组名'].apply(is_invalid_name)]

        class_summary = df.groupby('组别').agg({
            '作业减分': 'sum',
            '日常减分': 'sum',
            '迟到减分': 'sum',
        }).reset_index()

        result = []
        for _, row in class_summary.iterrows():
            result.append({
                "班级": row['组别'],
                "作业减分": row['作业减分'],
                "日常减分": row['日常减分'],
                "迟到减分": row['迟到减分']
            })
        return result
    except Exception as e:
        logger.error(f"分析失败: {str(e)}")
        raise

@app.get("/")
async def root():
    return {"msg": "Hello, API 正常运行"}

@app.get("/analyze")
async def analyze_api(url: str = Query(..., description="Excel文件的URL")):
    logger.info(f"收到GET分析请求: {url}")
    try:
        result = analyze_excel(url)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
