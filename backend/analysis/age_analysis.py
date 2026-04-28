"""
[담당 A] 연령별 트렌드 분석 스크립트 (스텁)
- backend/naverapi.py 와 동일한 패턴으로 .env 로드
- ages 파라미터를 [10대], [20대], [30대] 로 나눠 호출 후 비교 그래프 생성
- 결과는 web/images/age_trend.png 로 저장
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# TODO: 연령대별 반복 호출 → 비교 그래프
print("연령별 분석 — 구현 예정")
