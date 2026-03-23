from datetime import datetime

import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from loguru import logger

from core.config import get_time_zone
from modules.byp_analyze.service import analyze_excel_url
from modules.site_ops import is_feature_enabled

from .byp_analyze_schema import (
    BypAnalysisData,
    GetBypAnalyzeDataResponse,
    SingleClassAnalysisData,
    SingleStudentAnalysisData,
)


router = APIRouter()


@router.get("/", response_model=GetBypAnalyzeDataResponse, summary="分析班易评导出的 Excel")
async def analyze_api(url: str = Query(..., description="Excel 文件的 URL")):
    if not is_feature_enabled("toolkit_byp_analyze"):
        raise HTTPException(status_code=503, detail="BYP 分析工具当前未开放")
    logger.info("收到班易评分析请求: {}", url)
    try:
        result = await run_in_threadpool(analyze_excel_url, url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail="下载 Excel 失败: {}".format(exc))
    except Exception as exc:
        logger.exception("班易评分析失败: {}", exc)
        raise HTTPException(status_code=500, detail=str(exc))

    class_stat = [
        SingleClassAnalysisData(
            class_name=item.class_name,
            homework_deduction=item.homework_deduction,
            daily_deduction=item.daily_deduction,
            late_deduction=item.late_deduction,
        )
        for item in result.class_stat
    ]
    student_stat = [
        SingleStudentAnalysisData(
            student_name=item.student_name,
            total_add_score=item.total_add_score,
            rank=item.rank,
            bonus_details=item.bonus_details,
        )
        for item in result.student_stat
    ]

    return GetBypAnalyzeDataResponse(
        data=BypAnalysisData(
            response_at=datetime.now(tz=get_time_zone()),
            class_stat=class_stat,
            student_stat=student_stat,
        )
    )
