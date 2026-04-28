"""
[담당 B] 키워드 비교 분석 스크립트 (스텁)
- 키워드 그룹별 평균/최대 검색비율 막대 그래프
- 결과: web/images/keyword_compare.png
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

# TODO: data/trend_raw.csv 읽어서 groupby('keyword').agg() → bar chart
print("키워드 비교 — 구현 예정")
