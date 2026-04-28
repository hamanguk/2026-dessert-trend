"""
네이버 데이터랩 검색어 트렌드 수집 (조장 전용 실행 스크립트)
─────────────────────────────────────────────────────────
- 7개 SNS 유행 음식 키워드를 4가지 차원으로 수집:
    1. trend_raw.csv      : 시계열 (월별)
    2. trend_age.csv      : 연령대별 검색 비중
    3. trend_gender.csv   : 성별 검색 비중
    4. trend_device.csv   : 기기별(모바일/PC) 검색 비중
- 결과 CSV는 data/ 에 저장 → git push 하면 팀원이 pull로 받음
- 팀원은 .env 키 발급 안 해도 CSV로 작업 가능
"""

import os
import sys
import time
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # 헤드리스(GUI 없는) 백엔드 - 창 안 뜸
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "backend"))
from collect.keywords import ALL_BATCHES, AGE_GROUPS, GENDERS, DEVICES

load_dotenv(ROOT_DIR / ".env")
CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError(f".env 파일에서 키를 찾을 수 없습니다: {ROOT_DIR / '.env'}")

URL = "https://openapi.naver.com/v1/datalab/search"
HEADERS = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET,
    "Content-Type": "application/json",
}

START_DATE = "2025-05-01"
END_DATE = "2026-04-26"


def make_body(keyword_groups, time_unit="month", **filters):
    body = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "timeUnit": time_unit,
        "keywordGroups": keyword_groups,
    }
    body.update({k: v for k, v in filters.items() if v is not None})
    return body


def fetch(body):
    r = requests.post(URL, headers=HEADERS, json=body, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"❌ API 에러 {r.status_code}: {r.text}")
    return r.json()


def to_dataframe(payload, extra_cols=None):
    frames = []
    for group in payload["results"]:
        df = pd.DataFrame(group["data"])
        df["keyword"] = group["title"]
        if extra_cols:
            for col, val in extra_cols.items():
                df[col] = val
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def collect_dimension(filter_groups, dim_label, time_unit="month"):
    """연령/성별/기기 같은 필터 차원 데이터 수집"""
    all_dfs = []
    for label, codes in filter_groups:
        for batch in ALL_BATCHES:
            if dim_label == "age":
                payload = fetch(make_body(batch, time_unit, ages=codes))
            elif dim_label == "gender":
                payload = fetch(make_body(batch, time_unit, gender=codes))
            elif dim_label == "device":
                payload = fetch(make_body(batch, time_unit, device=codes))
            df = to_dataframe(payload, {dim_label: label})
            all_dfs.append(df)
            time.sleep(0.3)  # rate-limit 방지
    return pd.concat(all_dfs, ignore_index=True)


def main():
    data_dir = ROOT_DIR / "data"
    data_dir.mkdir(exist_ok=True)

    print("─" * 60)
    print("📡 1/4  시계열 데이터 수집 중...")
    raw_dfs = []
    for batch in ALL_BATCHES:
        payload = fetch(make_body(batch))
        raw_dfs.append(to_dataframe(payload))
        time.sleep(0.3)
    df_raw = pd.concat(raw_dfs, ignore_index=True)
    df_raw["period"] = pd.to_datetime(df_raw["period"])
    df_raw["ratio"] = df_raw["ratio"].astype(float)
    df_raw.to_csv(data_dir / "trend_raw.csv", index=False, encoding="utf-8-sig")
    print(f"   ✅ trend_raw.csv 저장 ({len(df_raw)}행)")

    print("📡 2/4  연령대별 데이터 수집 중...")
    df_age = collect_dimension(AGE_GROUPS, "age")
    df_age.to_csv(data_dir / "trend_age.csv", index=False, encoding="utf-8-sig")
    print(f"   ✅ trend_age.csv 저장 ({len(df_age)}행)")

    print("📡 3/4  성별 데이터 수집 중...")
    df_gender = collect_dimension(GENDERS, "gender")
    df_gender.to_csv(data_dir / "trend_gender.csv", index=False, encoding="utf-8-sig")
    print(f"   ✅ trend_gender.csv 저장 ({len(df_gender)}행)")

    print("📡 4/4  기기별 데이터 수집 중...")
    df_device = collect_dimension(DEVICES, "device")
    df_device.to_csv(data_dir / "trend_device.csv", index=False, encoding="utf-8-sig")
    print(f"   ✅ trend_device.csv 저장 ({len(df_device)}행)")

    # 검증용 미리보기 그래프 (조장 확인용)
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_raw, x="period", y="ratio", hue="keyword", marker="o")
    plt.title("2026 SNS 유행 음식 - 종합 검색 트렌드 (월별)", fontsize=15)
    plt.ylabel("검색 상대 비율")
    plt.xlabel("기간")
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    images_dir = ROOT_DIR / "web" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    out = images_dir / "00_overview.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"💾 검증용 그래프 저장: {out}")
    print("─" * 60)
    print("✅ 모든 데이터 수집 완료!")


if __name__ == "__main__":
    main()
