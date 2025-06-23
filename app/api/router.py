from fastapi import APIRouter
from api.byp_analyze import byp_analyze_api

api_router = APIRouter()
api_router.include_router(byp_analyze_api.router, prefix="/byp_analyze", tags=["班易评分析"])