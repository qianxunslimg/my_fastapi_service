from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional
from common.http_common_schema import *

class SingleClassAnalzeData(BaseModel):
    class_name: str = Field(description="类名")
    homework_deduction: int = Field(description="作业减分")
    daily_deduction: int = Field(description="日常减分")
    late_deduction: int = Field(description="迟到减分")

class SingleStudentAnalzeData(BaseModel):
    student_name: str = Field(description="学生姓名")
    total_add_score: int = Field(description="总加分")
    rank: int = Field(description="排名")
    bonus_details: str = Field(description="奖金明细")
    
class BypAnaSchema(BaseModel):
    response_at: datetime = Field(description="回复时间")
    class_stat: List[SingleClassAnalzeData] = Field(description="班级统计")
    student_stat: List[SingleStudentAnalzeData] = Field(description="学生统计")
    
GetBypAnalyzeDataResponse = CommonResponse[BypAnaSchema]