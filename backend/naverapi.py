"""
네이버 데이터랩 검색어 트렌드 수집 + 시각화
- API 키는 프로젝트 루트의 .env 파일에서 읽어옴
- 결과 그래프는 ../web/images/ 에 저장 (닷홈 업로드용)
"""

import os
from pathlib import Path

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

# ── 1. .env 로드 ──────────────────────────────────────
# 이 파일(backend/naverapi.py) 기준으로 한 단계 위(프로젝트 루트)의 .env 를 읽음
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError(
        ".env 파일에서 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 을 찾을 수 없습니다.\n"
        f"확인 경로: {ROOT_DIR / '.env'}"
    )

# ── 2. API 요청 ───────────────────────────────────────
URL = "https://openapi.naver.com/v1/datalab/search"
HEADERS = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET,
    "Content-Type": "application/json",
}

body = {
    "startDate": "2025-05-01",
    "endDate": "2026-04-26",
    "timeUnit": "month",
    "keywordGroups": [
        {"groupName": "우베(Ube)", "keywords": ["우베 디저트", "ube cake", "보라색 고구마"]},
        {"groupName": "저당/제로", "keywords": ["저당 케이크", "제로 슈가 디저트", "무설탕"]},
        {"groupName": "요거트/과일", "keywords": ["요아정", "과일 화채", "그릭요거트"]},
    ],
    "device": "mo",          # 모바일 트렌드 위주
    "ages": ["1", "2", "3"], # 10·20·30대
}

response = requests.post(URL, headers=HEADERS, json=body, timeout=10)

if response.status_code != 200:
    raise RuntimeError(f"❌ 네이버 API 에러: {response.status_code} / {response.text}")

# ── 3. 데이터 변환 ────────────────────────────────────
data = response.json()
frames = []
for group in data["results"]:
    df_group = pd.DataFrame(group["data"])
    df_group["keyword"] = group["title"]
    frames.append(df_group)

df = pd.concat(frames, ignore_index=True)
df["period"] = pd.to_datetime(df["period"])
df["ratio"] = df["ratio"].astype(float)

# 분석 단계에서 재사용할 수 있도록 CSV 로도 저장
data_dir = ROOT_DIR / "data"
data_dir.mkdir(exist_ok=True)
df.to_csv(data_dir / "trend_raw.csv", index=False, encoding="utf-8-sig")
print("✅ 데이터 수집 성공! data/trend_raw.csv 저장 완료")

# ── 4. 시각화 ─────────────────────────────────────────
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False
plt.figure(figsize=(12, 6))

sns.lineplot(data=df, x="period", y="ratio", hue="keyword", marker="o")
plt.title("데이터로 보는 2026 디저트 트렌드 흐름", fontsize=15)
plt.ylabel("검색 상대 비율")
plt.xlabel("기간")
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 닷홈에 업로드할 web/images/ 에 저장
images_dir = ROOT_DIR / "web" / "images"
images_dir.mkdir(parents=True, exist_ok=True)
output_path = images_dir / "trend_map_01.png"
plt.savefig(output_path, dpi=150)
print(f"💾 그래프 저장: {output_path}")
plt.show()
