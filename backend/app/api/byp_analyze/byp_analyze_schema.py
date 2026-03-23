from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from common.schemas import CommonResponse


class SingleClassAnalysisData(BaseModel):
    class_name: str = Field(description="班级名称")
    homework_deduction: int = Field(description="作业减分")
    daily_deduction: int = Field(description="日常减分")
    late_deduction: int = Field(description="迟到减分")


class SingleStudentAnalysisData(BaseModel):
    student_name: str = Field(description="学生姓名")
    total_add_score: int = Field(description="总加分")
    rank: int = Field(description="排名")
    bonus_details: str = Field(description="加分明细")


class BypAnalysisData(BaseModel):
    response_at: datetime = Field(description="响应时间")
    class_stat: List[SingleClassAnalysisData] = Field(default_factory=list, description="班级统计")
    student_stat: List[SingleStudentAnalysisData] = Field(default_factory=list, description="学生统计")


GetBypAnalyzeDataResponse = CommonResponse[BypAnalysisData]
