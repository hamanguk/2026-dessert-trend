"""
[담당 C] 기기별 트렌드 분석 스크립트 (스텁)
- device='pc' / 'mo' 두 번 호출하여 비교
- 결과: web/images/device_trend.png
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

# TODO: pc / mo 두 번 호출 → 동일 키워드의 채널별 비율 비교
print("기기별 트렌드 — 구현 예정")
