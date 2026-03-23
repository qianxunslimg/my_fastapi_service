from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import List

import pandas as pd
import requests
from loguru import logger

from core.config import settings


NAME_COLUMN = "姓名/组名"
GROUP_COLUMN = "组别"
HOMEWORK_COLUMN = "作业减分"
DAILY_COLUMN = "日常减分"
LATE_COLUMN = "迟到减分"
TOTAL_BONUS_COLUMN = "加分项总分"
TOP_STUDENT_LIMIT = 7
EXCLUDED_GROUP = "10DSE"

BONUS_COLUMN_ALIASES = {
    "不扣分“加分”": ("不扣分“加分”", '不扣分"加分"', "不扣分＂加分＂"),
    "不扣分“消分”": ("不扣分“消分”", '不扣分"消分"', "不扣分＂消分＂"),
    "勤学好问": ("勤学好问",),
    "课堂笔记": ("课堂笔记",),
}
SUMMARY_COLUMNS = (HOMEWORK_COLUMN, DAILY_COLUMN, LATE_COLUMN)


@dataclass(frozen=True)
class ClassAnalysis:
    class_name: str
    homework_deduction: int
    daily_deduction: int
    late_deduction: int


@dataclass(frozen=True)
class StudentAnalysis:
    student_name: str
    total_add_score: int
    rank: int
    bonus_details: str


@dataclass(frozen=True)
class BypAnalysisResult:
    class_stat: List[ClassAnalysis]
    student_stat: List[StudentAnalysis]


def analyze_excel_url(url):
    dataframe = _load_excel_dataframe(url)
    prepared_dataframe = _prepare_dataframe(dataframe)
    class_stat = _build_class_stat(prepared_dataframe)
    student_stat = _build_student_stat(prepared_dataframe)
    _log_analysis_result(class_stat, student_stat)
    return BypAnalysisResult(class_stat=class_stat, student_stat=student_stat)


def _load_excel_dataframe(url):
    response = requests.get(url, timeout=settings.EXTERNAL_REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return pd.read_excel(BytesIO(response.content))


def _prepare_dataframe(dataframe):
    _ensure_required_columns(dataframe, (NAME_COLUMN, GROUP_COLUMN))
    normalized = dataframe.copy()
    normalized = normalized[~normalized[NAME_COLUMN].apply(_is_invalid_name)].copy()

    for column in SUMMARY_COLUMNS:
        if column in normalized.columns:
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce").fillna(0)
        else:
            normalized[column] = 0

    for canonical_name, aliases in BONUS_COLUMN_ALIASES.items():
        source_name = _pick_existing_column(normalized, aliases)
        if source_name is None:
            normalized[canonical_name] = 0
            continue
        normalized[canonical_name] = pd.to_numeric(normalized[source_name], errors="coerce").fillna(0)

    normalized[TOTAL_BONUS_COLUMN] = normalized[list(BONUS_COLUMN_ALIASES.keys())].sum(axis=1)
    return normalized


def _ensure_required_columns(dataframe, required_columns):
    missing_columns = [column for column in required_columns if column not in dataframe.columns]
    if missing_columns:
        raise ValueError("Excel 缺少必要列: {}".format(", ".join(missing_columns)))


def _pick_existing_column(dataframe, aliases):
    for column_name in aliases:
        if column_name in dataframe.columns:
            return column_name
    return None


def _is_invalid_name(name):
    if pd.isna(name):
        return True
    text = str(name).strip()
    return ("班" in text and len(text) <= 3) or text.upper() == "DSE"


def _build_class_stat(dataframe):
    class_summary = (
        dataframe.groupby(GROUP_COLUMN)[list(SUMMARY_COLUMNS)]
        .sum()
        .reset_index()
        .sort_values(GROUP_COLUMN)
    )

    class_stat = []
    for _, row in class_summary.iterrows():
        class_stat.append(
            ClassAnalysis(
                class_name=str(row[GROUP_COLUMN]),
                homework_deduction=_to_int(row[HOMEWORK_COLUMN]),
                daily_deduction=_to_int(row[DAILY_COLUMN]),
                late_deduction=_to_int(row[LATE_COLUMN]),
            )
        )
    return class_stat


def _build_student_stat(dataframe):
    filtered = dataframe[dataframe[GROUP_COLUMN] != EXCLUDED_GROUP].copy()
    ranking_frame = filtered.nlargest(TOP_STUDENT_LIMIT, TOTAL_BONUS_COLUMN, keep="all")
    ranking_frame = ranking_frame[ranking_frame[TOTAL_BONUS_COLUMN] > 0].copy()
    if ranking_frame.empty:
        return []

    ranking_frame = ranking_frame.sort_values(TOTAL_BONUS_COLUMN, ascending=False)
    ranking_frame["rank"] = ranking_frame[TOTAL_BONUS_COLUMN].rank(method="min", ascending=False).astype(int)

    student_stat = []
    for _, row in ranking_frame.iterrows():
        student_stat.append(
            StudentAnalysis(
                student_name=str(row[NAME_COLUMN]).strip(),
                total_add_score=_to_int(row[TOTAL_BONUS_COLUMN]),
                rank=int(row["rank"]),
                bonus_details=_build_bonus_details(row),
            )
        )
    return student_stat


def _build_bonus_details(row):
    details = []
    for column_name in BONUS_COLUMN_ALIASES.keys():
        score = _to_int(row[column_name])
        if score > 0:
            details.append("{}:{}".format(column_name, score))
    return " + ".join(details) if details else "无加分项"


def _to_int(value):
    if pd.isna(value):
        return 0
    return int(float(value))


def _log_analysis_result(class_stat, student_stat):
    logger.info("班级统计完成，共 {} 个班级", len(class_stat))
    for item in class_stat:
        logger.info(
            "班级 {} -> 作业减分: {}, 日常减分: {}, 迟到减分: {}",
            item.class_name,
            item.homework_deduction,
            item.daily_deduction,
            item.late_deduction,
        )

    if not student_stat:
        logger.info("没有有效的加分记录")
        return

    logger.info("学生加分排行完成，共 {} 条记录", len(student_stat))
    for item in student_stat:
        logger.info("TOP{} {} -> {}", item.rank, item.student_name, item.total_add_score)
