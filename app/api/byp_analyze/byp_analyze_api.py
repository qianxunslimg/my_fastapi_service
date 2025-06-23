from fastapi import APIRouter, FastAPI, HTTPException, Query
from loguru import logger
import pandas as pd
import requests
from io import BytesIO
import os
import inspect
from .byp_analyze_schema import *
from core.config import get_time_zone

router = APIRouter()

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

def analyze_and_log(url):
    # 下载并读取Excel
    excel_file = download_excel(url)
    df = pd.read_excel(excel_file)

    # 清洗异常数据
    df = df[~df['姓名/组名'].apply(is_invalid_name)]

    # 转换加分列为数值类型，处理可能的格式问题
    bonus_cols = ['不扣分“加分”', '不扣分“消分”', '勤学好问', '课堂笔记']
    for col in bonus_cols:
        # 处理可能的引号格式不一致
        if col not in df.columns:
            alt_col = col.replace('"', '＂')  # 尝试全角引号
            if alt_col in df.columns:
                df[col] = df[alt_col]
            else:
                df[col] = 0
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 计算加分项总分
    df['加分项总分'] = df[bonus_cols].sum(axis=1)

    class_summary = df.groupby('组别').agg({
        '作业减分': 'sum',
        '日常减分': 'sum',
        '迟到减分': 'sum',
    }).reset_index()

    logger.info("======== 各班级数据统计 ========")
    for _, row in class_summary.iterrows():
        logger.info(f"班级 {row['组别']}：")
        logger.info(f"  作业减分总和：{row['作业减分']}")
        logger.info(f"  日常减分总和：{row['日常减分']}")
        logger.info(f"  迟到减分总和：{row['迟到减分']}")
        logger.info("----------------------------------")

    # 统计四个加分项的总分前七名
    logger.info("\n\n======= 加分项总分TOP7统计 =======")
    filtered_df = df[df['组别'] != '10DSE']

    # 获取前七名（包含并列）
    nlargest_df = filtered_df.nlargest(7, '加分项总分',
                                       keep='all')  # 只显示有加分的学生（总分>0）
    top_df = nlargest_df[['姓名/组名', '组别', '加分项总分'] + bonus_cols]
    top_df = top_df[top_df['加分项总分'] > 0]

    if not top_df.empty:
        logger.info("★★★ 加分项总分前七名学生 ★★★")
        # 计算排名（处理并列情况）
        top_df = top_df.sort_values('加分项总分', ascending=False)
        top_df['名次'] = top_df['加分项总分'].rank(method='min',
                                            ascending=False).astype(int)

        prev_rank = 0
        for _, row in top_df.iterrows():
            current_rank = row['名次']
            rank_display = str(current_rank)

            # 处理并列排名显示
            if current_rank == prev_rank:
                rank_display = f"并列{current_rank}"
            else:
                rank_display = f"{current_rank}名"

            # 构建加分项详情
            bonus_details = []
            for col in bonus_cols:
                if row[col] > 0:
                    bonus_details.append(f"{col}:{row[col]}")

            bonus_str = " + ".join(bonus_details) if bonus_details else "无加分项"

            # logger.info(f"{rank_display}: {row['姓名/组名']}（{row['组别']}）")
            # logger.info(f"   总分: {row['加分项总分']} = {bonus_str}")
            # 分数 姓名
            logger.info(f"{row['加分项总分']}: {row['姓名/组名']}")

            prev_rank = current_rank
    else:
        logger.info("⚠️ 没有有效的加分记录")

@router.get("/", response_model=GetBypAnalyzeDataResponse)
async def analyze_api(url: str = Query(..., description="Excel文件的URL")):
    logger.info(f"收到GET分析请求: {url}")
    try:
        class_stat = [] # List[SingleClassAnalzeData]
        excel_file = download_excel(url)
        df = pd.read_excel(excel_file)

        # 清洗异常数据
        df = df[~df['姓名/组名'].apply(is_invalid_name)]

        # 转换加分列为数值类型，处理可能的格式问题
        bonus_cols = ['不扣分“加分”', '不扣分“消分”', '勤学好问', '课堂笔记']
        for col in bonus_cols:
            # 处理可能的引号格式不一致
            if col not in df.columns:
                alt_col = col.replace('"', '＂')  # 尝试全角引号
                if alt_col in df.columns:
                    df[col] = df[alt_col]
                else:
                    df[col] = 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 计算加分项总分
        df['加分项总分'] = df[bonus_cols].sum(axis=1)

        class_summary = df.groupby('组别').agg({
            '作业减分': 'sum',
            '日常减分': 'sum',
            '迟到减分': 'sum',
        }).reset_index()

        logger.info("======== 各班级数据统计 ========")
        for _, row in class_summary.iterrows():
            logger.info(f"班级 {row['组别']}：")
            logger.info(f"  作业减分总和：{row['作业减分']}")
            logger.info(f"  日常减分总和：{row['日常减分']}")
            logger.info(f"  迟到减分总和：{row['迟到减分']}")
            logger.info("----------------------------------")
            class_stat.append(SingleClassAnalzeData(
                class_name=row['组别'],
                homework_deduction=row['作业减分'],
                daily_deduction=row['日常减分'],
                late_deduction=row['迟到减分']
            ))

        # 统计四个加分项的总分前七名
        student_stat = [] # List[SingleStudentAnalzeData]
        logger.info("\n\n======= 加分项总分TOP7统计 =======")
        filtered_df = df[df['组别'] != '10DSE']

        # 获取前七名（包含并列）
        nlargest_df = filtered_df.nlargest(7, '加分项总分',
                                        keep='all')  # 只显示有加分的学生（总分>0）
        top_df = nlargest_df[['姓名/组名', '组别', '加分项总分'] + bonus_cols]
        top_df = top_df[top_df['加分项总分'] > 0]

        if not top_df.empty:
            logger.info("★★★ 加分项总分前七名学生 ★★★")
            # 计算排名（处理并列情况）
            top_df = top_df.sort_values('加分项总分', ascending=False)
            top_df['名次'] = top_df['加分项总分'].rank(method='min',
                                                ascending=False).astype(int)

            prev_rank = 0
            for _, row in top_df.iterrows():
                current_rank = row['名次']
                rank_display = str(current_rank)

                # 处理并列排名显示
                if current_rank == prev_rank:
                    rank_display = f"并列{current_rank}"
                else:
                    rank_display = f"{current_rank}名"

                # 构建加分项详情
                bonus_details = []
                for col in bonus_cols:
                    if row[col] > 0:
                        bonus_details.append(f"{col}:{row[col]}")

                bonus_str = " + ".join(bonus_details) if bonus_details else "无加分项"
                logger.info(f"{row['加分项总分']}: {row['姓名/组名']}")
                student_stat.append(SingleStudentAnalzeData(
                    student_name=row['姓名/组名'],
                    total_add_score=row['加分项总分'],
                    bonus_details=bonus_str,
                    rank=current_rank,
                ))
                prev_rank = current_rank
        else:
            logger.info("⚠️ 没有有效的加分记录")
        return GetBypAnalyzeDataResponse(status = 200, message = "success", data = BypAnaSchema(class_stat=class_stat, student_stat=student_stat, response_at=datetime.now(tz=get_time_zone())))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))